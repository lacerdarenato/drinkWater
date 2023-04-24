from data import alchemy
from functools import reduce
import datetime


class DailyConsumptionModel(alchemy.Model):
    __tablename__ = 'daily_consumption'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    date = alchemy.Column(alchemy.String, nullable=False)
    remaining = alchemy.Column(alchemy.Integer)
    consumption = alchemy.Column(alchemy.Integer)
    percentage = alchemy.Column(alchemy.Integer)
    is_goal = alchemy.Column(alchemy.Boolean)

    person_id = alchemy.Column(
        alchemy.Integer, alchemy.ForeignKey('person.id'))

    def __init__(self, date, remaining,  consumption, percentage, is_goal, person_id):
        self.date = date
        self.remaining = remaining
        self.consumption = consumption
        self.percentage = percentage
        self.is_goal = is_goal
        self.person_id = person_id

    def json(self):
        return {
            'date': self.date,
            'remaining': self.remaining,
            'consumption': self.consumption,
            'percentage': self.percentage,
            'is_goal': self.is_goal,
            'person_id': self.person_id
        }

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    def sum_total_consumption_at(consumption_json):
        total = sum(item.json()['consumption'] for item in consumption_json if item)
        return total

    def set_consumption_params(self, consumption):
        self.consumption = consumption

    @classmethod
    def find_one_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_consumptions_by_id_at_date(cls, id, date):
        return cls.query.filter(
            DailyConsumptionModel.person_id == id,
            DailyConsumptionModel.date == date).all()
