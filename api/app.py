from flask import Flask, request, jsonify
from model import person, dailyConsumption
import datetime
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
    new_person = person.PersonModel(
        request_data['name'], request_data['weight'])
    new_person.save_to_db()
    result = person.PersonModel.find_one_by_id(new_person.id)

    return jsonify(result.json())


@app.route('/person/<int:id>/', methods=['GET'])
def get_person_by_id(id):
    result = person.PersonModel.find_one_by_id(id)
    if result:
        return result.json()
    return {'message': f'Pessoa com id: {id} nao existe'}, 404


@app.route('/person/<int:id>/consumption', methods=['POST'])
def create_consumption_for_person(id):
    request_data = request.get_json()

    if not 'date' in request_data:
        request_data['date'] = datetime.datetime.now().strftime('%d/%m/%Y')

    person_searched = person.PersonModel.find_one_by_id(id)
    if person_searched:
        new_consumption = dailyConsumption.DailyConsumptionModel(
            date=request_data['date'],
            remaining=request_data['remaining'],
            consumption=request_data['consumption'],
            percentage=request_data['percentage'],
            is_goal=request_data['is_goal'],
            person_id=person_searched.id)

        new_consumption.save_to_db()
        return new_consumption.json()

    return {'message': f'Pessoa com id: {id} nao encontrada'}, 404


if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    app.run(port=5000, debug=True)
