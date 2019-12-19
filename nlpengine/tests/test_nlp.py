import unittest
import pytest


# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    # def test_two(self):
    #     x = "hello"
    #     assert hasattr(x, "check")
# class NLPEngineAppTest(unittest.TestCase):


# def test_get_intents(self):
#     engine = NLPEngine()
#     data = engine.extract_intents("QUe cursos hay?", 1)
#     self.assertEqual(data, {
#         "prediction": "__label__listarCursos",
#         "probability": 0.9001758098602295
#     })
