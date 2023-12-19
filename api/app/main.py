from fastapi import FastAPI
from os import environ
from app.core.config import setup_configuration, setup_logging
from app.api import endpoint_router
import logging
from dotenv import load_dotenv


def create_app(config_class: object) -> FastAPI:
    app = FastAPI()
    setup_logging(config_class)

    # Routes
    app.include_router(endpoint_router)

    return app


try:
    load_dotenv()
except Exception as e:
    print(f'Error loading environment variables: {e}')

env = environ.get('API_ENVIRONMENT', 'development').lower()
config_class = setup_configuration(env)
app = create_app(config_class)
