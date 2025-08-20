import logging

from flask import Flask

from app import create_app

logging.basicConfig(level=logging.DEBUG)

app: Flask = create_app()

if __name__ == "__main__":
    app.run()
