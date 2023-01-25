import requests
import time
import os
import json


from datecommunication import settings


def writ_app_data_to_file(data):
    lifetime_token = data.get("expires_in", 3600)    # время жизни access токена
    data["expires_in"] = time.time() + float(lifetime_token) - 5 * 60   # время по истечении которого обновляется токен

    # сохранение данных авторизации в файл
    with open(os.path.join(settings.BASE_DIR, 'secrets.json'), 'w') as secrets_file:
        json.dump(data, secrets_file)
