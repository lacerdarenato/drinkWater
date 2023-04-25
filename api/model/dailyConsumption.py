from data import alchemy


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

    def __init__(self, date, remaining, person_id):
        self.date = date
        self.remaining = remaining
        self.consumption = 0
        self.percentage = 0
        self.is_goal = False
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

    def update_to_db(self, consumption, percentage, remaining, is_goal):
        self.consumption = consumption
        self.percentage = percentage
        self.remaining = remaining
        self.is_goal = is_goal

    @classmethod
    def find_all_person_consumption(cls, person_id):
        return cls.query.filter_by(person_id=person_id).all()

    @ classmethod
    def find_one_consumption(cls, person_id, date):
        return cls.query.filter(
            DailyConsumptionModel.person_id == person_id,
            DailyConsumptionModel.date == date).first()
