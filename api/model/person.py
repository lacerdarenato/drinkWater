from data import alchemy
from . import dailyConsumption


class PersonModel(alchemy.Model):
    __tablename__ = 'person'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(255))
    weight = alchemy.Column(alchemy.Integer)
    daily_consumption = alchemy.relationship(
        dailyConsumption.DailyConsumptionModel, lazy='dynamic')

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'weight': self.weight
        }

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    @classmethod
    def find_one_by_id(cls, id):
        cls.query.filter_by(id=id).first()

    @classmethod
    def find_one_by_name(cls, name):
        cls.query.filter_by(name=name).first()
