#!/bin/bash

gunicorn -c gunicorn_conf.py app.app:app
