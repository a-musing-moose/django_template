#! /bin/bash
set -e

UVICORN_LOG_LEVEL="${UVICORN_LOG_LEVEL:-info}"
WEB_CONCURRENCY="${WEB_CONCURRENCY:-4}"

serve () {
    exec uvicorn \
        --workers="$WEB_CONCURRENCY" \
        --lifespan=off \
        --host=0.0.0.0 \
        --port=8000 \
        --ws=none \
        --no-use-colors \
        --access-log \
        --log-level="$UVICORN_LOG_LEVEL" \
        {{ cookiecutter.project_slug }}.asgi:application
}

if [ -z "$1" ] # nothing specified so we bootstrap the service itself
then
    manage migrate --noinput
    serve
elif [ "$1" = "run" ]  # run the service only
then
    serve
elif [ "$1" = "migrate" ]  # run database migrations
then
    exec manage migrate --noinput "${@:2}"
elif [ "$1" = "bash" ]  # run a regular bash shell
then
    exec bash "${@:2}"
else # pass any other params directly to manage.py to handle
    exec manage "$@"
fi
