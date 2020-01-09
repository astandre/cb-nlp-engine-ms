from kbsbot.nlpengine.app import create_app
from kbsbot.nlpengine.database import db, init_database
import sys
import signal
import os


def _quit(signal, frame):
    print("Bye!")
    # add any cleanup code here
    sys.exit(0)


def main():
    app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)

    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)

    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()

    app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
else:
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    app = create_app(settings=_SETTINGS)
    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()
