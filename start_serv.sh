#!/bin/bash
source /home/vader/python/src/github.com/jay13jay/larry-venv/bin/activate
exec gunicorn -w 2 -k gevent -b 127.0.0.1:5000 api:app
