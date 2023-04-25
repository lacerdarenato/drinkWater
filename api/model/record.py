from data import alchemy
from . import person

import datetime


class RecordModel(alchemy.Model):
    __tablename__ = 'record'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    date = alchemy.Column(alchemy.String(10), nullable=False)
    amount = alchemy.Column(alchemy.Integer)

    person_id = alchemy.Column(
        alchemy.Integer, alchemy.ForeignKey('person.id'))

    def __init__(self, date, amount, person_id):
        self.date = date
        self.amount = amount
        self.person_id = person_id

    def json(self):
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount,
        }

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    @classmethod
    def get_daily_drunk_by_person(cls, id, date):
        daily_records = cls.query.filter(
            RecordModel.person_id == id,
            RecordModel.date == date).all()
        return sum(record.json()['amount'] for record in daily_records if record)
