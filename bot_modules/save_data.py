import os
import json


list_users = {}
abspath = os.path.abspath(__file__+'/../../users.json')
with open(abspath, 'r') as file:
    list_users = json.load(file)
print(list_users)
def save_users():
    with open(abspath, "w") as file:
        json.dump(list_users, file, indent=4, ensure_ascii=False)