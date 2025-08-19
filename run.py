import logging

from flask import Flask

from app import create_app
from app.job import run_job

logging.basicConfig(level=logging.DEBUG)

app: Flask = create_app()
run_job()

if __name__ == "__main__":
    app.run()
