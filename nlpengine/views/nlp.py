from flakon import JsonBlueprint
from flask import request
from nlp_main import NLPEngine

nlp = JsonBlueprint('nlp', __name__)
engine = NLPEngine()


@nlp.route('/entities', methods=['POST'])
def get_entities():
    """Extract entities

    This view will extract all intents using trained fasttext model for cursos
    """
    if request.method == 'POST':
        data = request.get_json()
        if "k" in data:
            entities = engine.extract_entities(data["sentence"], data["k"])
        else:
            entities = engine.extract_entities(data["sentence"])
        return entities
    else:
        return {'message': 'method not allowed here',
                'status': 405}


@nlp.route('/intents', methods=['POST'])
def get_intents():
    """Extract intents

    This view will extract all entities using trained fasttext model for courses
    @param
    """
    if request.method == 'POST':
        data = request.get_json()
        if "k" in data:
            entities = engine.extract_intents(data["sentence"], data["k"])
        else:
            entities = engine.extract_intents(data["sentence"])
        return entities
    else:
        return {'message': 'method not allowed here',
                'status': 405}
