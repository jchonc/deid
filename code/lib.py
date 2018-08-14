"""Main function library code goes here"""
import spacy

class DeidentificationHandler:
    """the main process class"""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        if 'ner' not in self.nlp.pipe_names:
            ner = self.nlp.create_pipe('ner')
            self.nlp.add_pipe(ner, last=True)

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
                inpStr = inpStr.replace(entity.text, dateNew)

#            elif entity.label_ ==


        return inpStr



def de_identify_text(input_string):
    """de-identify the given input text"""
    return input_string
