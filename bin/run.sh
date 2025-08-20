#!/bin/bash
set -e

if [ ! -d "migrations" ]; then
    echo "初始化数据库迁移目录"
    flask db init
fi


echo "对比差异"
flask db migrate -m "init"
echo "执行数据库迁移"
flask db upgrade


echo "启动 Gunicorn"
gunicorn -c gunicorn.py run:app
