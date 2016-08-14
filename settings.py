import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BROKER_TRANSPORT_OPTIONS = os.environ.get('BROKER_TRANSPORT_OPTIONS')
CELERY_RESULT_BACKEND    = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_IMPORTS = ('queue.enqueue',)

BROKER_URL = os.environ.get('BROKER_URL')
api_key    = os.environ.get('APIKEY')
base_url   = os.environ.get('BASE_URL')
