import os

from datetime import datetime


date = datetime.now()

if os.path.exists("/root/Pictures"):
    storage_path = "/root/Pictures"
else:
    storage_path = "."

storage_path = f"{storage_path}/{date.strftime('%Y/%m/%d')}".replace("/", os.sep)

if not os.path.exists(storage_path):
    os.makedirs(storage_path)