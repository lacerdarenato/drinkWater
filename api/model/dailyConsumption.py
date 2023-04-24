from data import alchemy
from record import RecordModel
from person import PersonModel

import datetime


class DailyConsumptionModel(alchemy.Model):
    __tablename__ = 'daily_consumption'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    date = alchemy.Column(alchemy.String(10), nullable=False)
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
    
    def update_to_db(self):
        alchemy.session.update(self)
        alchemy.session.commit()

    def sum_total_consumption_at(self, daily_records):
        total_consumption = sum(
            record.json()['consumption'] for record in daily_records if record)
        return total_consumption

    @classmethod
    def find_one_consumption(cls, person_id, date):
        return cls.query.filter(
            DailyConsumptionModel.person_id == person_id,
            DailyConsumptionModel.date == date).first()
