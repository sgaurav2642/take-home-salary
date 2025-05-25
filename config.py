import json

# Load JSON config
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# Access values
APP_NAME = config_data["APP_NAME"]
APP_SOURCE = config_data["APP_SOURCE"]
USER_ID = config_data["USER_ID"]
PASSWORD = config_data["PASSWORD"]
USER_KEY = config_data["USER_KEY"]
ENCRYPTION_KEY = config_data["ENCRYPTION_KEY"]
AUTH_TOKEN = config_data["AUTH_TOKEN"]
PIN = config_data["PIN"]
BASE_URL = config_data["BASE_URL"]
DB_NAME = config_data["DB_NAME"]
DB_USER = config_data["DB_USER"]
DB_PASSWORD = config_data["DB_PASSWORD"]
DB_HOST = config_data["DB_HOST"]
DB_PORT = config_data["DB_PORT"]
CLIENT_CODE=config_data["CLIENT_CODE"]