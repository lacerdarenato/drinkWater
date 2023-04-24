from flask import Flask, request, jsonify
from model.dailyConsumption import DailyConsumptionModel
from model.person import PersonModel
from model.record import RecordModel
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
    new_person = PersonModel(
        request_data['name'], request_data['weight'])
    new_person.save_to_db()
    result = PersonModel.find_one_by_id(new_person.id)

    return jsonify(result.json())


@app.route('/person/<int:id>/', methods=['GET'])
def get_person_by_id(id):
    result = PersonModel.find_one_by_id(id)
    if result:
        return result.json()
    return {'message': f'Pessoa com id: {id} nao existe'}, 404


@app.route('/person/<int:id>/consumption', methods=['POST'])
def create_consumption_for_person(id):
    request_data = request.get_json()

    if not 'date' in request_data:
        request_data['date'] = datetime.datetime.now().strftime('%d/%m/%Y')

    person_searched = PersonModel.find_one_by_id(id)
    if person_searched:
        new_consumption = DailyConsumptionModel(
            date=request_data['date'],
            remaining=request_data['remaining'],
            consumption=request_data['consumption'],
            percentage=request_data['percentage'],
            is_goal=request_data['is_goal'],
            person_id=person_searched.id)

        new_consumption.save_to_db()
        return new_consumption.json()

    return {'message': f'Pessoa com id: {id} nao encontrada'}, 404


@app.route('/consumption/<int:id>', methods=['POST'])
def drink_water(id):
    request_data = request.get_json()

    if not 'date' in request_data:
        request_data['date'] = datetime.datetime.now().strftime('%d/%m/%Y')

    person_searched = PersonModel.find_one_by_id(id)
    if person_searched:
        new_record = RecordModel(
            date=request_data['date'],
            amount=request_data['amount'],
            person_id=request_data['person_id']
        )
        consumption_searched = DailyConsumptionModel.find_one_consumption(person_searched.id)
        daily_consumption = new_record.get_daily_drunk_by_person(person_searched.id, request_data['date'])
        target = person_searched.target
        remaining = target - daily_consumption,

        new_consumption = DailyConsumptionModel(
            date=request_data['date'],
            consumption=daily_consumption,
            remaining=remaining,
            percentage=remaining/target,
            is_goal=True if remaining >= target else False)
        if consumption_searched:
            new_record.save_to_db()
            new_consumption.update_to_db()
        else:
            new_record.save_to_db()
            new_consumption.save_to_db()


        return new_record.json()

    return {'message': f'Pessoa com id: {id} nao encontrada'}, 404


if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    app.run(port=5000, debug=True)
