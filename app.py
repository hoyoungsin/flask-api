from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase("devilfruits", user="hoyoungsin", password="", host="localhost", port="5432")

class BaseModel(Model):
    class Meta:
        database = db

class DevilFruit(BaseModel):
    name = CharField()
    type = CharField()
    current_user = TextField()

db.connect()
db.drop_tables([DevilFruit])
db.create_tables([DevilFruit])

DevilFruit(name='Gomu-Gomu no Mi', type='Paramecia', current_user='Monkey D. Luffy').save()

app = Flask(__name__)


@app.route('/')
def index():
    return "Devil Fruits!"

app.run(port=5000, debug=True)


@app.route('/devilfruits/', methods=['GET', 'POST'])
@app.route('/devilfruits/<name>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(name=None):
    if request.method == 'GET':
        if name:
            return jsonify(model_to_dict(DevilFruit.get(DevilFruit.name == name)))
        else:
            devilfruit_list = []
            for devilfruit in DevilFruit.select():
                devilfruit_list.append(model_to_dict(devilfruit))
            return jsonify(devilfruit_list)

    if request.method == 'POST':
        new_devilfruit = dict_to_model(DevilFruit, request.get_json())
        new_devilfruit.save()
        return jsonify({'success': True})
    
    if request.method == 'PUT':
        body = request.get_json()
        DevilFruit.update(body).where(DevilFruit.name == name).execute()
        return f"{name} has been updated"