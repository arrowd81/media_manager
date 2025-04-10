import os

from dotenv import load_dotenv

load_dotenv()

# SECRETS
JWT_SECRET_KEY = os.getenv('JWT_SECRET')

RDBMS_URL = 'sqlite:///test.sqlite'
anime_list_proxy = {
    'http': 'http://127.0.0.1:8889',
    'https': 'http://127.0.0.1:8889',
}
