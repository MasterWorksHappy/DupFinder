# __init__.py

from flask import Flask

from dupRunner.dupRunner import dupRunner


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(dupRunner)
    return app


if __name__ == "__main__":
    app = create_app(debug=True)
    app.run(use_debugger=True, use_reloader=True)
