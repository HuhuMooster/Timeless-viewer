from flask import render_template, url_for, request
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
    seeds = request.form.get("seed")
    socket_ids = request.form.get("socketID")
    title = f"Timeless jewel viewer: {name}"
    title += f" {seeds}" if seeds else ""
    
    for socket_id in socket_ids.split(','):
        if socket_id and not (1 <= int(socket_id) <= 21):
            continue
        for seed in seeds.split(','):
            search_dict = {}
            for field, value in zip(["name", "seed", "socket_id"], [name, int(seed) if seed else None, int(socket_id) if socket_id else None]):
                if value is not None:
                    search_dict[field] = value
            for jewel in mongo.db.jewels.find(search_dict):
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
