from kbsbot.nlpengine.nlp_main import *
from unittest import TestCase
from kbsbot.nlpengine.app import create_app
from kbsbot.nlpengine.database import *

import json


class NLPTest(TestCase):

    def setUp(self):
        self.intent_engine = NLPEngine("opencampus_intents.ftz")
        self.entity_engine = NLPEngine("opencampus_cursos.ftz")

    def test_intents(self):
        result = self.intent_engine.extract_information(sentence="Que cursos hay", model_type=ModelType.intent)
        assert "intent" in result

    def test_entities(self):
        result = self.entity_engine.extract_information(
            sentence="Cuando inicia el curso de emprendimiento y generacion de ideas", model_type=ModelType.entities)
        assert "entities" in result


class TestAPP(TestCase):

    # this method is run before each test
    def setUp(self):
        app = create_app()
        self.client = app.test_client()
        db.init_app(app)
        db.app = app
        db.create_all(app=app)
        agent = Agent(name='opencampuscursos')
        intent_model = Model(name='opencampus_intents.ftz', url='asdasd', model_type=ModelType.intent, agent=agent)
        cursos_model = Model(name='opencampus_cursos.ftz', url='asdasd', model_type=ModelType.entities,
                             entity_name="CURSOS",
                             agent=agent)

        db.session.add(agent)
        db.session.add(intent_model)
        db.session.add(cursos_model)
        db.session.commit()

    # this method is run after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_intent(self):
        data = dict(
            sentence="De que se trata el curso emprendimiento",
            agent="opencampuscursos"

        )
        response = self.client.post(
            '/intents', data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(data_resp["intent"]) >= 1)

    def test_get_entities(self):
        data = dict(
            sentence="emprendimiento y genracion de ideas",
            agent="opencampuscursos"

        )
        response = self.client.post(
            '/entities', data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(data_resp["entities"]) >= 1)
