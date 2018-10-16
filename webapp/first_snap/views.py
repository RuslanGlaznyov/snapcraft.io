import os
import flask
from ruamel.yaml import YAML, YAMLError

dir = os.path.dirname(os.path.realpath(__file__))

yaml = YAML(typ="safe")

first_snap = flask.Blueprint(
    "fist_snap_flow",
    __name__,
    template_folder="/templates",
    static_folder="/static",
)


@first_snap.route("/<language>")
def get_language(language):
    context = {"language": language}
    return flask.render_template(
        "first-snap/install-snapcraft.html", **context
    )


@first_snap.route("/<language>/<operating_system>/package")
def get_package(language, operating_system):
    filename = "".join(["../../first-snap/", language, "/package.yaml"])

    filepath = os.path.join(dir, filename)

    try:
        with open(filepath, "r") as stream:
            steps = yaml.load(stream)
    except YAMLError as error:
        return flask.abort(404)

    context = {"language": language, "os": operating_system, "steps": steps}

    return flask.render_template("first-snap/package.html", **context)


@first_snap.route("/<language>/<operating_system>/build")
def get_build(language, operating_system):
    filename = "".join(["../../first-snap/", language, "/build.yaml"])

    filepath = os.path.join(dir, filename)

    try:
        with open(filepath, "r") as stream:
            steps = yaml.load(stream)
    except YAMLError as error:
        return flask.abort(404)

    operating_system_only = operating_system.split("-")[0]
    install_type = operating_system.split("-")[1]

    context = {
        "language": language,
        "os": operating_system,
        "steps": steps[operating_system_only][install_type],
    }

    return flask.render_template("first-snap/build.html", **context)


@first_snap.route("/<language>/<operating_system>/test")
def get_test(language, operating_system):
    filename = "".join(["../../first-snap/", language, "/test.yaml"])

    filepath = os.path.join(dir, filename)

    try:
        with open(filepath, "r") as stream:
            steps = yaml.load(stream)
    except YAMLError as error:
        return flask.abort(404)

    operating_system_only = operating_system.split("-")[0]

    context = {
        "language": language,
        "os": operating_system,
        "steps": steps[operating_system_only],
    }

    return flask.render_template("first-snap/test.html", **context)


@first_snap.route("/<language>/<operating_system>/push")
def get_push(language, operating_system):
    filename = "".join(["../../first-snap/", language, "/package.yaml"])

    filepath = os.path.join(dir, filename)

    try:
        with open(filepath, "r") as stream:
            data = yaml.load(stream)
    except YAMLError as error:
        return flask.abort(404)

    flask_user = flask.session["openid"]

    if "nickname" in flask_user:
        user = {
            "image": flask_user["image"],
            "username": flask_user["nickname"],
            "display_name": flask_user["fullname"],
            "email": flask_user["email"],
        }
    else:
        user = None

    context = {
        "language": language,
        "os": operating_system,
        "user": user,
        "snap_name": data["name"],
    }

    return flask.render_template("first-snap/push.html", **context)
