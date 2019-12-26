#!/bin/sh
exec uvicorn src.app:app\
  --host "${API_HOST}"\
  --port "${API_PORT}"\
  "$@"
