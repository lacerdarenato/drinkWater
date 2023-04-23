from flask import Flask, request, jsonify
from model import person, dailyConsumption
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXEPTION'] = True


@app.before_first_request
def create_tables():
    alchemy.create_all()


@app.route('/', methods=['GET'])
def home():
    return 'API funcionando', 200


@app.route('/person', methods=['POST'])
def create_person():
    request_data = request.get_json()
    new_person = person.PersonModel(request_data['name'], request_data['weight'])
    new_person.save_to_db()
    result = person.PersonModel.find_one_by_id(new_person.id)
    
    return jsonify(result.json())
    


if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    app.run(port=5000, debug=True)
