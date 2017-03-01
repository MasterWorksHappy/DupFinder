# __init__.py

# import sys
# import os
# print "\n\n\n(sys.executable)\n", (sys.executable)
# print "\n\n\n(sys.path)\n", (sys.path)
# print "\n\n\n(os.getcwd())\n", (os.getcwd())

import logging
from logging.config import fileConfig
from flask import Flask


fileConfig('DupDestroyer.ini')
logger = logging.getLogger('dupDestroyer')
logger.setLevel(logging.DEBUG)

from dupRunner.dupRunner import dupRunner


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(dupRunner)
    return app


if __name__ == "__main__":

    app = create_app(debug=False)
    app.run(use_debugger=False, use_reloader=False)
