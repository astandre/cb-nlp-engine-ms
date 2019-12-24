import unittest
import pytest
from kbsbot.nlpengine.database import *
from kbsbot.nlpengine.nlp_main import *

from unittest import TestCase
from flask_webtest import TestApp
import json


# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x


class NLPTest(TestCase):

    def setUp(self):
        self.engine = NLPEngine("opencampus_intents.ftz")

    def test_intents(self):
        result = self.engine.extract_information(sentence="Que cursos hay", model_type=ModelType.intent)
        print(result)

        assert "intent" in result
