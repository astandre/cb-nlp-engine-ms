import fasttext
import unicodedata
import re
from .database import ModelType
import os
import spacy

nlp = spacy.load("es_core_news_sm")


class NLPEngine:
    """NLP Engine
    A custom class to encapsulate a fasttext model.

    Attributes:
        :param @model_url: Name of the model
    """
    model = None

    def __init__(self, model_url):
        """
        Args:
            :param @model_url: Name of the model
        """
        try:
            self.model_url = os.path.dirname(__file__) + "/nlp_models/" + model_url
            self.model = fasttext.load_model(self.model_url)
        except Exception as e:
            print(e)
            print("Error")
            path = os.path.dirname(__file__) + "/nlp_models"
            if not os.path.exists(path):
                os.makedirs(path)
                print("Models must be installed")

    @staticmethod
    def clean_sentence(sentence):
        """

        This method removes all special characters, special characters and ticks

        Args:
            @param: sentence:  A sentence to be cleaned


        Returns:
            A new sentence in a normalized way

    """
        sentence = sentence.lower()
        sentence = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))
        sentence = (re.sub(r"[^a-zA-Z0-9]+", ' ', sentence))
        return sentence

    def extract_information(self, sentence, threshold=0.0, name=None, k=1, model_type=ModelType.intent):
        """
        This method extracts information depending of the model type
        Args:
            @param: sentence:  A sentence where information will be extracted

            @param: name:  The name of the entity type.

            @param: k:  Number of results to be found

            @param: model_type:  If model is for intents or entities

        Returns:
            A dict containing information found in sentence
        """
        results = self.model.predict(self.clean_sentence(sentence), k=k, threshold=threshold)
        final = []
        for label, prob in zip(results[0], results[1]):
            if name is not None:
                final.append(
                    {"prediction": label.replace("__label__", "http://127.0.0.1/ockb/resources/"), "label": label,
                     "probability": prob, "entity": name})
            else:
                final.append(
                    {"prediction": label.replace("__label__", "http://127.0.0.1/ockb/resources/"), "label": label,
                     "probability": prob})
        if model_type == ModelType.intent:
            return {"intent": final}
        elif model_type == ModelType.entities:
            return {"entities": final}


def get_generic_entities(sentence):
    result = []
    doc = nlp(sentence)
    entities = doc.ents
    for ent in entities:
        # print(ent.text, ent.label_)
        result.append({"label": ent.text, "entity": ent.label_})
    return result


class AgentNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self, "Must provide a valid agent name")


class ModelNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self, "No models found related to agent")
