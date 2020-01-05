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
    name = str(request.form.get("name")).title()
    seed = request.form.get("seed")
    seed = int(seed) if seed else None
    socket_id = request.form.get("socketID")
    socket_id = int(socket_id) if socket_id and 1 <= int(socket_id) <= 21 else None
    title = f"Timeless jewel viewer: {name}"
    title += f" #{seed}" if seed else ""

    search_dict = {}
    for field, value in zip(["name", "seed", "socket_id"], [name, seed, socket_id]):
        if value is not None:
            search_dict[field] = value

    jewels = mongo.db.jewels.find(search_dict)
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
