#!/bin/bash
source ../zndt_env/bin/activate
export FLASK_APP=app
export FLASK_DEBUG=1
flask run --host=0.0.0.0