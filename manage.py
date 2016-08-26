from flask import Flask, url_for
from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls

from dupRunner.dupRunner import dupRunner

app = Flask(__name__)
app.register_blueprint(dupRunner)
manager = Manager(app)


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote(
            "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line


manager.add_command("urls", ShowUrls())

if __name__ == "__main__":
    manager.run()
