import logging

from flask import Flask

from app import create_app
from app.job import run_job

logging.basicConfig(level=logging.DEBUG)

app: Flask = create_app()
logging.warning(app.config.get('RUN_MODE'))
if app.config.get('RUN_MODE') != 'migration':
    run_job()

if __name__ == "__main__":
    app.run()
