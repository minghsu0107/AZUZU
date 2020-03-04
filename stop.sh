#!/usr/bin/env bash
# shut down uwsgi
uwsgi --stop ./uwsgi7070.pid
# gracefully stop nginx
sudo nginx -s quit