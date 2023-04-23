from data import alchemy


class PersonModel(alchemy.Model):
    __tablename__ = 'person'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(255))
    weight = alchemy.Column(alchemy.Integer)
    dailyConsumption = []

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'weight': self.weight
        }
