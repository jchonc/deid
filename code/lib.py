"""Main function library code goes here"""
import re
import spacy
import html2text
import datetime
from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer

def modifiedTokenizer(nlp):
    """Modify the existing Tokenizer to better tokenize phone numbers and URLs"""
    # prefix
    pNum_prefixes = r'^[\(]'
    url_prefixes = r'''^[\[\("']'''
    all_prefixes_re = spacy.util.compile_prefix_regex(tuple(list(nlp.Defaults.prefixes) + [pNum_prefixes,url_prefixes]))

    # infix
    pNum_infixes = r'[\)-]'
    url_infixes = r'''[-~]'''
    infix_re = spacy.util.compile_infix_regex(tuple(list(nlp.Defaults.infixes) + [pNum_infixes,url_infixes]))

    # suffix
    url_suffixes = r'''[\]\)"']$'''
    suffix_re = spacy.util.compile_suffix_regex(tuple(list(nlp.Defaults.suffixes) + [url_suffixes]))  

    # token match
    url_re = re.compile(r'''^https?://''')

    return Tokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
                     prefix_search = all_prefixes_re.search, 
                     infix_finditer = infix_re.finditer, suffix_search = suffix_re.search,
                     token_match=url_re.match)

def mask_text(input, sub_input, filt_expr, mask_char):
    """Using regex to replace numbers/letters without changing format"""
    return input.replace(sub_input, re.sub(filt_expr,mask_char,sub_input))

def is_date(date_string):
    """Check if matchup is a date and not an ID/MRN"""
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"]
    for dateFormat in date_formats:
        try:
            validateDate = datetime.datetime.strptime(date_string, dateFormat)
        except ValueError:
            if date_formats.index(dateFormat) == 2:
                return False
            else:
                continue
    return True

class DeidentificationHandler:
    """the main process class"""
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.tokenizer = modifiedTokenizer(self.nlp)
        if 'ner' not in self.nlp.pipe_names:
            ner = self.nlp.create_pipe('ner')
            self.nlp.add_pipe(ner, last=True)

        # phone number Matcher
        self.pNumMatcher = Matcher(self.nlp.vocab)
        pNumPattern = [{'ORTH': '(', 'OP': '?'}, {'SHAPE': 'ddd'}, 
                       {'ORTH': ')', 'OP': '?'}, {'ORTH': '-', 'OP': '?'}, 
                       {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
        self.pNumMatcher.add('PHONE_NUMBER', None, pNumPattern)

        # email Matcher
        self.emailMatcher = Matcher(self.nlp.vocab)
        email_flag = lambda text: bool(re.compile(r"^[^@]+@[^@]+\.[^@]+$").match(text))
        IS_EMAIL = self.nlp.vocab.add_flag(email_flag)
        self.emailMatcher.add('EMAIL', None, [{IS_EMAIL: True}])

        # IP Address Matcher (IPv4 and IPv6)
        self.ipMatcher = Matcher(self.nlp.vocab)
        # ipv4_flag
        ipv4_flag = lambda text: bool(re.compile(r"(?:25[0-5]|2[0-4]\d|1?\d{1,2}\.){4}").match(text))
        IS_IPV4 = self.nlp.vocab.add_flag(ipv4_flag)
        self.ipMatcher.add('IPV4', None, [{IS_IPV4: True}])
        # ipv6_flag (untested)
        ipv6_flag = lambda text: bool(re.compile(r"([0-9A-F]{1,4}:){8}").match(text))
        IS_IPV6 = self.nlp.vocab.add_flag(ipv6_flag)
        self.ipMatcher.add('IPV6', None, [{IS_IPV6: True}])

        # URL Matcher
        self.urlMatcher = Matcher(self.nlp.vocab)
        url_flag = lambda text: bool(re.compile(r"https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,}").match(text))
        IS_URL_ADDRESS = self.nlp.vocab.add_flag(url_flag)
        self.urlMatcher.add('URL_ADDRESS', None, [{IS_URL_ADDRESS: True}])

        # HTML Parser
        self.tag_processor = html2text.HTML2Text()
        self.tag_processor.ignore_links = True

    def __del__(self):
        self.nlp = None

    def normalize_text(self, input_string):
        """extract the text from HTML tags"""
        return self.tag_processor.handle(input_string).rstrip()

    def process_text(self, input_string):
        """Mask the part of text we need to redact"""
        inpStr = input_string
        doc = self.nlp(inpStr)

        # Replace any matching IDs with 9 and Z (done separately with regex)
        idMatches = re.findall(r'#?(?:[A-Z0-9]-*){8,}',inpStr)
        for match in idMatches:
            if is_date(match):
                continue
            elif bool(re.search(r'\d',match)):
                match_replace = match
                match_replace = re.sub(r'\d','9',match_replace)
                match_replace = re.sub(r'[A-Z]','Z',match_replace)
                inpStr = inpStr.replace(match,match_replace)

        # Check doc.ents for any caught entities
        for entity in doc.ents:
            # Is entity a person?
            if entity.label_ == 'PERSON':
                # Replace each letter with X
                inpStr = mask_text(inpStr, entity.text, r'\w', 'X')

            # Is entity a date or time?
            elif entity.label_ == 'DATE' or entity.label_ == 'TIME':
                # Replace all digits with 9
                inpStr = mask_text(inpStr, entity.text, r'\d', '9')

        # Replace any matching phone numbers with 9
        pNumMatches = self.pNumMatcher(doc)
        for match_id, start, end in pNumMatches:
            span = doc[start:end]
            inpStr = mask_text(inpStr, span.text, r'\d', '9')
        
        # Replace any matching emails with X
        emailMatches = self.emailMatcher(doc)
        for match_id, start, end in emailMatches:
            span = doc[start:end]
            inpStr = mask_text(inpStr, span.text, r'\w', 'X')

        # Replace any matching IP addresses with 9
        ipMatches = self.ipMatcher(doc)
        for match_id, start, end in ipMatches:
            span = doc[start:end]
            inpStr = mask_text(inpStr, span.text, r'\d', '9')
        
        # Replace any matching URLs with [url]
        urlMatches = self.urlMatcher(doc)
        for match_id, start, end in urlMatches:
            span = doc[start:end]
            inpStr = inpStr.replace(span.text, '[url]')

        return inpStr



def de_identify_text(input_string):
    """de-identify the given input text"""
    return input_string
