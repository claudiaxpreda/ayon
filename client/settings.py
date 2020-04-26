import os
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path)

SERVER_HOST=os.getenv('SERVER_HOST')
SERVER_PORT=os.getenv('SERVER_PORT')

URL_SERVER='http://{host}:{port}/api'.format(host=SERVER_HOST, port=SERVER_PORT)