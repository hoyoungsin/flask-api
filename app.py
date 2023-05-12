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
    ability = TextField()
    current_user = TextField()

db.connect()
db.drop_tables([DevilFruit])
db.create_tables([DevilFruit])

DevilFruit(name='Gomu Gomu no Mi', type='Paramecia', ability='Turns the user body into rubber, giving them the power to stretch, bounce, and inflate, as well as making them immune to electricity and near impervious to blunt-force attacks and bullets.', current_user='Monkey D. Luffy').save()
DevilFruit(name='Hito Hito no Mi: Model Nika', type='Zoam', ability='Allows the user to become an incarnation of the sun god Nika, granting them a rubber body that allows them to fight however they like, as well as granting them the ability to invoke joy in those around them.', current_user='Monkey D. Luffy').save()
DevilFruit(name='Bara Bara no Mi', type='Paramecia', ability='Allows the user to split their body into separate pieces, which they can manipulate and levitate through the air. It also makes them immune to slashing attacks.', current_user='Buggy').save()
DevilFruit(name='Hito Hito no Mi', type='Zoan', ability='Allows an animal that eats it to become a full human or a half-human hybrid, as well as grant them human-like intelligence and the ability to speak.', current_user='Tony Chopper')
DevilFruit(name='Mera Mera no Mi', type='Logia', ability='Allows the user to create, control, and transform into fire.', current_user='Sabo').save()
DevilFruit(name='Hana Hana no Mi', type='Paramecia', ability='Allows the user to sprout duplicates of their body parts from any nearby surface. The user maintains full control of duplicated limbs and can perceive sights and sounds remotely through duplicate eyes and ears.', current_user='Nico Robin').save()
DevilFruit(name='Yomi Yomi no Mi', type='Paramecia', ability='Allows the users soul to return to the living world after dying, bringing the user back to life. The user can also make their returned soul temporarily leave their reanimated body and their soul exudes a freezing coldness that can be weaponized.', current_user='Brook').save()
DevilFruit(name='Yami Yami no Mi', type='Logia', ability='Allows the user to create, control, and transform into darkness. The darkness has strong gravitational properties, and the user has an infinite amount of space inside of their elemental body.', current_user='Marshall D. Teach').save()
DevilFruit(name='Gura Gura no Mi', type='Paramecia', ability='Allows the user to create quakes and shockwaves. Considered to be the most powerful Paramecia.', current_user='Marshall D. Teach').save()
DevilFruit(name='Uo Uo no Mi: Seiryu', type='Zoan', ability=' Allows the user to become a full Azure Dragon or a half-Azure Dragon hybrid.', current_user='Kaidou').save()

app = Flask(__name__)

app.run(port=5000, debug=True)

@app.route('/')
def index():
    return "Devil Fruits!"

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
    
    if request.method == 'DELETE':
        DevilFruit.delete().where(DevilFruit.name == name).execute()
        return f"{name} has been deleted"
    