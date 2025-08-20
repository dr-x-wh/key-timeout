#!/bin/bash

echo "对比差异"
flask db migrate -m "init"
echo "执行数据库迁移"
flask db upgrade

echo "启动 Gunicorn"
gunicorn -c gunicorn.py run:app
