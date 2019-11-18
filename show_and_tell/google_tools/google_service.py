import os
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_JSON_FILE = os.environ.get("FN_SERVICE_JSON_FILE", default=False)
SERVICE_KEY = os.environ.get("FN_SERVICE_KEY", default=False)


def build_credentials(scopes):
    return ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_JSON_FILE, scopes=scopes)
