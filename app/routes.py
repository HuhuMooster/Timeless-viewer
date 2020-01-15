import json

from flask import render_template, request, url_for
from flask_pymongo import PyMongo
import pymongo
from fuzzywuzzy import fuzz

from app import app


def load_from_json(filename):
    try:
        with open(f"{filename}.json", 'r+') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        data = {}
    return data

mongo = PyMongo(app)
summed_mods = load_from_json("summed_mods")

@app.route('/')
def index():
    title = 'Timeless jewel viewer'
    return render_template("index.html", title=title)

@app.route('/search', methods=['POST'])
def search():
    jewels = []
    name = str(request.form.get("name")).title()
    seeds = request.form.get("seed")
    socket_ids = request.form.get("socketID")
    affix = request.form.get("affix")
    threshold = request.form.get("threshold")
    mod = ""
    
    title = f"Timeless jewel viewer: {name}"
    title += f" {seeds}" if seeds else ""

    if affix:
        mod = search_by_affix(affix)
        if threshold:
            threshold = float(threshold)
        else:
            threshold = 0
    
    for socket_id in socket_ids.split(','):
        if socket_id and not (1 <= int(socket_id) <= 21):
            continue
        for seed in seeds.split(','):
            search_dict = {}
            for field, value in zip(["name", "seed", "socket_id", f'summed.{mod}' if mod else None], [name, int(seed) if seed else None, int(socket_id) if socket_id else None, {"$gte": threshold} if threshold else None]):
                if field is not None and value is not None:
                    search_dict[field] = value
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
    for mod in summed_mods.values():
        simplified_mod = mod.lower()
        ratio = fuzz.partial_ratio(affix, simplified_mod)
        if ratio > best_ratio:
            best_ratio = ratio
            best_mod = mod

    return best_mod