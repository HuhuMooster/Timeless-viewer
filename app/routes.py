import os

import pymongo
from flask import current_app as app
from flask import render_template, request, send_from_directory
from flask_pymongo import PyMongo

from app import app

mongo = PyMongo(app)

@app.route('/')
def index():
    title = 'Timeless jewel viewer'
    return render_template("index.html", title=title)

@app.route('/search', methods=['POST'])
def search():
    jewels = []
    name = str(request.form.get("name")).title()
    seeds = request.form.get("seeds")
    socket_ids = request.form.get("socketIDs")
    affixes = request.form.getlist("affixes")
    thresholds = request.form.getlist("thresholds")
    latest = request.form.get("latest")

    CONSTRAINTS = {
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
    JEWEL_SOCKETS_COUNT = 21
    MAX_JEWEL_COUNT = int(
        CONSTRAINTS.get("Brutal Restraint").get("max") - CONSTRAINTS.get("Brutal Restraint").get("min") +
        (CONSTRAINTS.get("Elegant Hubris").get("max") / 10) - (CONSTRAINTS.get("Elegant Hubris").get("min") / 10) +
        CONSTRAINTS.get("Glorious Vanity").get("max") - CONSTRAINTS.get("Glorious Vanity").get("min") +
        CONSTRAINTS.get("Lethal Pride").get("max") - CONSTRAINTS.get("Lethal Pride").get("min") +
        CONSTRAINTS.get("Militant Faith").get("max") - CONSTRAINTS.get("Militant Faith").get("min")
    )
    
    search_terms = {
        "name": name,
        "seeds": seeds,
        "socket_ids": socket_ids,
        "affixes": affixes,
        "thresholds": thresholds,
        "latest": latest
    }

    if latest:
        sockets_count = len(socket_ids.split(','))
        sockets_count = sockets_count if sockets_count >= 1 else JEWEL_SOCKETS_COUNT
        latest = int(latest) * sockets_count
    else:
        latest = MAX_JEWEL_COUNT * JEWEL_SOCKETS_COUNT

    title = f"Timeless jewel viewer: {name}"
    title += f" {seeds}" if seeds else ""

    affixes_thresholds = {}
    for affix, threshold in zip(affixes, thresholds):
        if affix:
            affixes_thresholds[f'summed.{affix}'] = {"$gte": float(threshold)} if threshold else {'$gte': 0.01}
    
    for socket_id in socket_ids.split(','):
        # skip if socket_id is not valid
        if socket_id and not (1 <= int(socket_id) <= 21):
            continue
        for seed in seeds.split(','):
            # skip if seed is not within the roll range
            if seed != "" and not (CONSTRAINTS.get(name).get("min") <= int(seed) <= CONSTRAINTS.get(name).get("max")):
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

            for jewel in mongo.db.jewels.find(search_dict).sort([("$natural", -1)]).limit(latest):
                jewels.append(jewel)

    return render_template("index.html", title=title, search_terms=search_terms, jewels=jewels)

@app.route('/analyzed', methods=['GET'])
def analyzed():
    title = "Analyzed by date"
    latest_additions = {}
    for jewel in mongo.db.jewels.find().sort([("$natural", -1)]):
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.png', mimetype='image/vnd.microsoft.icon')
