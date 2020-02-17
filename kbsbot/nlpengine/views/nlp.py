from flakon import JsonBlueprint
from flask import request
from kbsbot.nlpengine.database import Model, ModelType, Agent
from kbsbot.nlpengine.nlp_main import *
import logging

nlp = JsonBlueprint('nlp', __name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@nlp.route('/status', methods=["GET"])
def get_status():
    return {"message": "ok"}


@nlp.route('/entities', methods=['POST'])
def get_entities():
    """

    This view will extract all entities using models associated with agent.

    Args:
        @param: agent:  A valid agent name.

        @param: sentence:  Sentence where information will be extracted.

        @param: k:  Number of predictions to be extracted.

    Returns:
        Entities found in sentence from different models

    Raises:
      ModelNotFoundException: If model not found

      AgentNotFoundException: If agent not found

      KeyError: If no correct keys in json request

    """

    data = request.get_json()
    logger.info(">>>>> Incoming data  %s", data)
    try:
        agent = Agent.query.filter_by(name=data["agent"]).first()
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
            result["entities"] += \
                engine.extract_information(data["sentence"], model.threshold, name=model.entity_name, k=k,
                                           model_type=ModelType.entities)["entities"]
        # print(result)
        result["status"] = 200
        logger.info("<<<<< Output  %s", result)
        return result
    except KeyError:
        return {'message': 'Must provide a valid agent name', 'status': 404}
    except AgentNotFoundException as e:
        return {'message': e.__str__(), 'status': 404}
    except ModelNotFoundException as e:
        return {'message': e.__str__(), 'status': 400}


@nlp.route('/intents', methods=['POST'])
def get_intents():
    """

    This view will extract intents using a trained model with fasttext.

    Args:
        @param: agent:  A valid agent name.

        @param: sentence:  Sentence where information will be extracted.

        @param: k:  Number of predictions to be extracted.

    Returns:
        Entities found in sentence from different models

    Raises:
      ModelNotFoundException: If model not found

      AgentNotFoundException: If agent not found

      KeyError: If no correct keys in json request
    """

    data = request.get_json()
    logger.info(">>>>> Incoming data  %s", data)
    try:
        agent = Agent.query.filter_by(name=data["agent"]).first()
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
        result = engine.extract_information(data["sentence"], model.threshold, k=k, model_type=ModelType.intent)
        # print(result)
        result["status"] = 200
        logger.info("<<<<< Output  %s", result)
        return result
    except KeyError:
        return {'message': 'Must provide a valid agent name', 'status': 404}
    except AgentNotFoundException as e:
        return {'message': e.__str__(), 'status': 404}
    except ModelNotFoundException as e:
        return {'message': e.__str__(), 'status': 400}
