#!/usr/bin/env bash

if [ "$2" = '' ]; then
    set -- "${@:1:2}" "up"
fi

case $1 in
    db)
        docker-compose \
            -f _docker/compose/pg-db.yml \
            $(echo "$2")
        ;;
    app)
        docker-compose \
            -f _docker/compose/pg-db.yml \
            -f _docker/compose/web.yml \
            -f _docker/compose/nginx.yml \
            $(echo "$2")
        ;;
    *)
        echo "**********************************************************************************"
        echo -e "\e[31m*^*^*  error command must be sh _assist/dev.sh db|app up|pull|build  *^*^*\e[0m"
        echo "**********************************************************************************"
        ;;

esac
