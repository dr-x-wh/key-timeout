#!/bin/bash

if [ -d "migrations" ]; then
    echo "数据库迁移已初始化"
else
    flask db init
fi

flask db migrate -m "init"
flask db upgrade

gunicorn -c gunicorn.py run:app
