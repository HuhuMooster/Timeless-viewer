import os
from pprint import pprint

from bson import ObjectId, json_util
from pymongo import MongoClient


def import_from_json():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_timeless_db = MongoClient('mongodb://localhost:27017/')['project_timeless']
    timeless_db = MongoClient('mongodb://localhost:27017/')['timeless']

    print("Importing...")

    project_timeless_db.jewels.drop()

    with open(f'{current_dir}\\project_timeless.json', 'r') as f:
        for line in f:
            json_line = json_util.loads(line)
            project_timeless_db["jewels"].insert_one(json_line)

    print("Project_timeless database import done.")
    timeless_db.jewels.drop()

    with open(f'{current_dir}\\timeless.json', 'r') as f:
        for line in f:
            json_line = json_util.loads(line)
            timeless_db["jewels"].insert_one(json_line)

    print("Timeless database import done.")


if __name__ == "__main__":
    import_from_json()
