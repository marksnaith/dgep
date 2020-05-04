#!/bin/bash

/etc/init.d/nginx start
uwsgi --ini /app/dgep.ini
