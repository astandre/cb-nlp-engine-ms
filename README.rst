nlpengine
============

This microservice is  intended to extract structured information from raw text, to identify intents and entities for KBS bot.


This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.


.. image:: https://travis-ci.org/astandre/cb-nlp-engine-ms.svg?branch=master
    :target: https://travis-ci.org/astandre/cb-nlp-engine-ms

.. image:: https://readthedocs.org/projects/cb-nlp-engine-ms/badge/?version=latest
    :target: https://cb-nlp-engine-ms.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Running scripts


``docker build -t kbsbot/nlp_engine . -f docker/Dockerfile``


``docker run --rm  --name=nlp_engine -p 5001:8000 -it kbsbot/nlp_engine``





