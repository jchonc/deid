"""Main function library code goes here"""
import re
import spacy
from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer

def modifiedTokenizer(nlp):
    """Modify the existing Tokenizer to better tokenize phone numbers"""
    # prefix
    pNum_prefix = r'^[\(]'
    all_prefixes_re = spacy.util.compile_prefix_regex(tuple(list(nlp.Defaults.prefixes) + [pNum_prefix]))

    # infix
    pNum_infixes = r'[\)-]'
    infix_re = spacy.util.compile_infix_regex(tuple(list(nlp.Defaults.infixes) + [pNum_infixes]))

    # suffix
    suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)  

    return Tokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
                     prefix_search = all_prefixes_re.search, 
                     infix_finditer = infix_re.finditer, suffix_search = suffix_re.search,
                     token_match=None)

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

    def __del__(self):
        self.nlp = None

    def process_text(self, input_string):
        """Mask the part of text we need to redact"""
        inpStr = input_string
        doc = self.nlp(inpStr)
        # doc.ents contains all the NER results - assuming it is good
        # Change person names for each ents if is person
        # Change dates
        # Using regular expression to scan long meaningless strings
        for entity in doc.ents:
            # Is entity a person?
            if entity.label_ == 'PERSON':
                # Replace each letter with X
                nameNew = ''
                nameReplace = entity.text.split(" ")
                for nameComponent in nameReplace:
                    nameNew += len(nameComponent)*"X"+' '
                inpStr = inpStr.replace(entity.text, nameNew.rstrip(' '))

            # Is entity a date or time?
            elif entity.label_ == 'DATE' or entity.label_ == 'TIME':
                # Replace all digits with 9
                dateNew = ''
                dateReplace = entity.text
                for dateChar in dateReplace:
                    if dateChar.isdigit():
                        dateNew += '9'
                    else:
                        dateNew += dateChar
                inpStr = inpStr.replace(dateReplace, dateNew)
        
        # Replace any matching phone numbers with 9
        pNumMatches = self.pNumMatcher(doc)
        for match_id, start, end in pNumMatches:
            span = doc[start:end]
            pNumNew = ''
            pNumReplace = span.text
            for pNumChar in pNumReplace:
                if pNumChar.isdigit():
                    pNumNew += '9'
                else:
                    pNumNew += pNumChar
            inpStr = inpStr.replace(pNumReplace, pNumNew)
        
        # Replace any matching emails with X
        emailMatches = self.emailMatcher(doc)
        for match_id, start, end in emailMatches:
            span = doc[start:end]
            emailNew = ''
            emailReplace = span.text
            for emailChar in emailReplace:
                if emailChar != '@' or emailChar != '.':
                    emailNew += 'X'
                else:
                    emailNew += emailChar
            inpStr = inpStr.replace(emailReplace, emailNew)


        return inpStr



def de_identify_text(input_string):
    """de-identify the given input text"""
    return input_string
