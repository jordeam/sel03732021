#!/bin/bash

python3 -m venv auth

source auth/bin/activate


export FLASK_APP=project

export FLASK_DEBUG=1


flask run --host 0.0.0.0

