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
        doc = self.nlp(input_string)
        entities = doc.ents

        # Change person names
        # Change dates
        # Using regular expression to scan long meaningless strings

        return input_string



def de_identify_text(input_string):
    """de-identify the given input text"""
    return input_string
