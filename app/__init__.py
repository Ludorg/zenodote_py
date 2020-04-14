#
# Project: Zenodote
# Filename: __init__.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/11/10
# https://ludorg.net/
#
# This work is licensed under the MIT License.
# See the LICENSE file in the root directory of this source tree.
#

import os

from flask import Flask

# Flask application for Zenodote (based on Flask tutorial)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        #
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "zndt.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from app import db

    db.init_app(app)

    from app import zndt_isbn
    app.register_blueprint(zndt_isbn.bp)
    app.add_url_rule("/", endpoint="index")

    return app
