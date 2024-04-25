#!/bin/bash

export NB_GRAPH_PASSWORD=$(cat /run/secrets/db_user_password)

uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port ${NB_API_PORT:-8000}
