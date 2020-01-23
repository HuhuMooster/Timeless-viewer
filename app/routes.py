import json

from flask import render_template, request, url_for, jsonify
from flask_pymongo import PyMongo
import pymongo
from fuzzywuzzy import fuzz

from app import app


mongo = PyMongo(app)
summed_mods = []
with open("affixes.txt") as f:
    for line in f.readlines():
        summed_mods.append(line[:-1])

@app.route('/')
def index():
    title = 'Timeless jewel viewer'
    if request.method == "POST":
        return jsonify(request.form)
    return render_template("index.html", title=title)

@app.route('/search', methods=['POST'])
def search():
    jewels = []
    name = str(request.form.get("name")).title()
    seeds = request.form.get("seeds")
    socket_ids = request.form.get("socketIDs")
    affixes = request.form.getlist("affixes")
    thresholds = request.form.getlist("thresholds")
    
    title = f"Timeless jewel viewer: {name}"
    title += f" {seeds}" if seeds else ""

    constraints = {
        "Brutal Restraint": {
            "min": 500,
            "max": 8000
        },
        "Elegant Hubris": {
            "min": 2000,
            "max": 160000
        },
        "Glorious Vanity": {
            "min": 100,
            "max": 8000
        },
        "Lethal Pride": {
            "min": 10000,
            "max": 18000
        },
        "Militant Faith": {
            "min": 2000,
            "max": 10000
        }
    }

    affixes_thresholds = {}
    for affix, threshold in zip(affixes, thresholds):
        if affix:
            affixes_thresholds[f'summed.{affix}'] = {"$gte": float(threshold)} if threshold else {'$gte': 0.01}
    
    for socket_id in socket_ids.split(','):
        # skip if socket_id is not valid
        if socket_id and not (1 <= int(socket_id) <= 21):
            continue
        for seed in seeds.split(','):
            # skip if seed is not within roll range
            if seed != "" and not (constraints.get(name).get("min") <= int(seed) <= constraints.get(name).get("max")):
                continue
            if seed != "" and name == "Elegant Hubris" and (int(seed) % 10 != 0):
                continue

            search_dict = {}
            search_dict["name"] = name
            if seed:
                search_dict["seed"] = int(seed)
            if socket_id:
                search_dict["socket_id"] = int(socket_id)
            search_dict.update(affixes_thresholds)

            for jewel in mongo.db.jewels.find(search_dict).sort("created", pymongo.DESCENDING):
                jewels.append(jewel)

    return render_template("index.html", title=title, jewels=jewels)

@app.route('/analyzed', methods=['GET'])
def analyzed():
    title = "Analyzed by date"
    latest_additions = {}
    for jewel in mongo.db.jewels.find():
        date = jewel['created'].strftime("%d.%m.%Y.")
        name = jewel['name']
        seed = jewel['seed']
        if date not in latest_additions.keys():
            latest_additions[date] = {}
        if name not in latest_additions[date].keys():
            latest_additions[date][name] = []
        if seed not in latest_additions[date][name]:
            latest_additions[date][name].append(seed)

    return render_template("analyzed.html", title=title, latest_additions=latest_additions)


def search_by_affix(affix):
    best_ratio = 0
    best_mod = ""
    for mod in summed_mods:
        simplified_mod = mod.lower()
        ratio = fuzz.partial_ratio(affix, simplified_mod)
        if ratio > best_ratio:
            best_ratio = ratio
            best_mod = mod

    return best_mod