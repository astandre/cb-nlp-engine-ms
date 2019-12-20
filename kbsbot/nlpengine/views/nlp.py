from flakon import JsonBlueprint
from flask import request
from kbsbot.nlpengine.database import Model, ModelType, Agent
from kbsbot.nlpengine.nlp_main import *

nlp = JsonBlueprint('nlp', __name__)


@nlp.route('/entities', methods=['POST'])
def get_entities():
    """Extract entities

    This view will extract all intents using trained fasttext model for cursos
    """
    if request.method == 'POST':
        data = request.get_json()
        try:
            agent = Agent.query.filter_by(name=data["agent"].lower()).first()
            print(agent)
            if agent is None:
                raise AgentNotFoundException()
            entities_model = Model.query.filter_by(agent=agent, model_type=ModelType.entities).all()
            if entities_model is None or len(entities_model) == 0:
                raise ModelNotFoundException()
            print(entities_model[0].name)
            engine = NLPEngine(entities_model[0].name)
            k = 1
            if "k" in data:
                k = data["k"]
            result = engine.extract_information(data["sentence"], k)
            print(result)
            return result
        except KeyError:
            return {'message': 'Must provide a valid agent name', 'status': 404}
        except AgentNotFoundException as e:
            return {'message': e.__str__(), 'status': 404}
        except ModelNotFoundException as e:
            return {'message': e.__str__(), 'status': 400}

        # if "k" in data:
        #     entities = engine.extract_entities(data["sentence"], data["k"])
        # else:
        #     entities = engine.extract_entities(data["sentence"])
        # return entities
    else:
        return {'message': 'method not allowed here',
                'status': 405}

#
# @nlp.route('/intents', methods=['POST'])
# def get_intents():
#     """Extract intents
#
#     This view will extract all entities using trained fasttext model for courses
#     @param
#     """
#     if request.method == 'POST':
#         data = request.get_json()
#         if "k" in data:
#             entities = engine.extract_intents(data["sentence"], data["k"])
#         else:
#             entities = engine.extract_intents(data["sentence"])
#         return entities
#     else:
#         return {'message': 'method not allowed here',
#                 'status': 405}
