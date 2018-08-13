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
            if entity.label_ == 'PERSON':
                nameNew = ''
                nameReplace = entity.text.split(" ")
                for nameComponent in nameReplace:
                    nameNew += len(nameComponent)*"X"+' '
                inpStr = inpStr.replace(entity.text, nameNew.rstrip(' '))
            elif entity.label_ == 'DATE':
                dateNew = ''
                dateReplace = entity.text.split("-")
                for dateComponent in dateReplace:
                    dateNew += len(dateComponent)*"9"+'-'
                inpStr = inpStr.replace(entity.text, dateNew.rstrip('-'))
            elif entity.label_ == 'TIME':
                timeNew = ''
                timeReplace = entity.text
                for timeChar in timeReplace:
                    if timeChar.isdigit():
                        timeNew += '9'
                    else:
                        timeNew += timeChar
                inpStr = inpStr.replace(entity.text, timeNew)




        return inpStr



def de_identify_text(input_string):
    """de-identify the given input text"""
    return input_string
