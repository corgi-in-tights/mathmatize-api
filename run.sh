# !/bin/bash
set -o allexport
source .env
set +o allexport

python3 ping/app.py runserver 0.0.0.0:8017