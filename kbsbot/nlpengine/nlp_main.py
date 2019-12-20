import fasttext
import unicodedata
import re


class NLPEngine:
    """NLP Engine
    This class encapsulates the models used to classify information from sentences.

    """

    def __init__(self, model_url):
        try:
            self.model_url = "./nlp_models/" + model_url
            print(model_url)
            self.model = fasttext.load_model(self.model_url)
            # self.entities_model = fasttext.load_model("nlp_models/opencampus_cursos.ftz")
        except Exception as  e:
            print(e)
            print("Error")

    @staticmethod
    def clean_sentence(sentence):
        """Clean sentence
        This method lowers all letters and drops especial characters from users input
        """
        sentence = sentence.lower()
        sentence = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))
        sentence = (re.sub(r"[^a-zA-Z0-9]+", ' ', sentence))
        return sentence

    def extract_information(self, sentence, k=1):
        results = self.model.predict(self.clean_sentence(sentence), k=k)
        final = []
        for label, prob in zip(results[0], results[1]):
            final.append({"prediction": label, "probability": prob})
        return {"labels": final}


class AgentNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self, "Must provide a valid agent name")


class ModelNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self, "No models found related to agent")
#
# def extract_entities(self, sentence, k=1):
#     return self.extract_information(sentence, self.entities_model, k)
#
# def extract_intents(self, sentence, k=1):
#     return self.extract_information(sentence, self.intents_model, k)
