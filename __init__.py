# __init__.py

import logging
from logging.config import fileConfig

from flask import Flask

from dupRunner.dupRunner import dupRunner

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(dupRunner)
    return app


def log_stuff():
    fileConfig('DupFinder.ini')
    logger = logging.getLogger('dupDestroyer')
    # logging.getLogger().addHandler(logging.NullHandler())

if __name__ == "__main__":
    log_stuff()
    app = create_app(debug=True)
    app.run(use_debugger=True, use_reloader=False)
