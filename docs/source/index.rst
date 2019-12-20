NLPENGINE
=========


This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.


The application is created with :func:`flakon.create_app`:

.. literalinclude:: ../../kbsbot/nlpengine/app.py


The :file:`settings.ini` file which is passed to :func:`create_app`
contains options for running the Flask app, like the DEBUG flag:

.. literalinclude:: ../../nlpengine/settings.ini
   :language: ini


Blueprint are imported from :mod:`nlpengine.views` and one
Blueprint and view example was provided in :file:`nlpengine/views/nlp.py`:

.. literalinclude:: ../../nlpengine/views/nlp.py
   :name: nlp.py
   :emphasize-lines: 13


Views can return simple mappings (as highlighted in the example above),
in that case they will be converted into a JSON response.

.. toctree::
   :maxdepth: 2

   api
