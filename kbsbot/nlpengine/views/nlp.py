from flakon import JsonBlueprint
from flask import request
from kbsbot.nlpengine.database import Model, ModelType, Agent
from kbsbot.nlpengine.nlp_main import *

nlp = JsonBlueprint('nlp', __name__)


@nlp.route('/entities', methods=['POST'])
def get_entities():
    """Extract entities

    This view will extract all entities using entity models associated with agent.
    This models must be trained with fasttext.
    @param: agent: agent name
    """
    if request.method == 'POST':
        data = request.get_json()
        try:
            agent = Agent.query.filter_by(name=data["agent"].lower()).first()
            # print(agent)
            if agent is None:
                raise AgentNotFoundException()
            entities_model = Model.query.filter_by(agent=agent, model_type=ModelType.entities).all()
            if entities_model is None or len(entities_model) == 0:
                raise ModelNotFoundException()
            result = {"entities": []}
            for model in entities_model:
                # print(model.name)
                engine = NLPEngine(model.name)
                k = 1
                if "k" in data:
                    k = data["k"]
                result["entities"] += engine.extract_information(data["sentence"], name=model.entity_name.upper(), k=k,
                                                                 model_type=ModelType.entities)["entities"]
            print(result)
            return result
        except KeyError:
            return {'message': 'Must provide a valid agent name', 'status': 404}
        except AgentNotFoundException as e:
            return {'message': e.__str__(), 'status': 404}
        except ModelNotFoundException as e:
            return {'message': e.__str__(), 'status': 400}
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
        try:
            agent = Agent.query.filter_by(name=data["agent"].lower()).first()
            # print(agent)
            if agent is None:
                raise AgentNotFoundException()
            model = Model.query.filter_by(agent=agent, model_type=ModelType.intent).first()
            if model is None:
                raise ModelNotFoundException()
            # print(model.name)
            engine = NLPEngine(model.name)
            k = 1
            if "k" in data:
                k = data["k"]
            result = engine.extract_information(data["sentence"], k=k, model_type=ModelType.intent)
            # print(result)
            return result
        except KeyError:
            return {'message': 'Must provide a valid agent name', 'status': 404}
        except AgentNotFoundException as e:
            return {'message': e.__str__(), 'status': 404}
        except ModelNotFoundException as e:
            return {'message': e.__str__(), 'status': 400}
    else:
        return {'message': 'method not allowed here',
                'status': 405}
