import fasttext
import unicodedata
import re


class NLPEngine:
    """NLP Engine
    This class encapsulates the models used to classify information from sentences.

    """

    def __init__(self):
        self.intents_model = fasttext.load_model("./models/opencampus_intents.ftz")
        self.entities_model = fasttext.load_model("./models/opencampus_entities.ftz")

    @staticmethod
    def clean_sentence(sentence):
        """Clean sentence
        This method lowers all letters and drops especial characters from users input
        """
        sentence = sentence.lower()
        sentence = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))
        sentence = (re.sub(r"[^a-zA-Z0-9]+", ' ', sentence))
        return sentence

    def extract_information(self, sentence, model, k=1):
        results = model.predict(self.clean_sentence(sentence), k=k)
        final = []
        for label, prob in zip(results[0], results[1]):
            final.append({"prediction": label, "probability": prob})
        return {"labels": final}

    def extract_entities(self, sentence, k=1):
        return self.extract_information(sentence, self.entities_model, k)

    def extract_intents(self, sentence, k=1):
        return self.extract_information(sentence, self.intents_model, k)
