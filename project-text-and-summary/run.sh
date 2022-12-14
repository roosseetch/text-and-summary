#!/bin/sh

if [ $START_CELERY_WORKER = 1 ] ; then
    echo "Starting celery worker"
    export CELERY_APP_MODULE=${CELERY_APP_MODULE-app.main:celery}
    poetry run celery -A "$CELERY_APP_MODULE" worker -l info --pool=prefork
    return 0
fi

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8001}


# run gunicorn
exec gunicorn --bind $HOST:$PORT "$APP_MODULE" -k uvicorn.workers.UvicornWorker
