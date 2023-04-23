from data import alchemy


class DailyConsumptionModel(alchemy.Model):
    id = alchemy.Column(alchemy.Integer, primary_key=True)
    date = alchemy.Column(alchemy.Date, nullable=False)
    target = alchemy.Column(alchemy.Integer)
    remaining = alchemy.Column(alchemy.Integer)
    consumption = alchemy.Column(alchemy.Integer)
    percentage = alchemy.Column(alchemy.Integer)
    is_goal = alchemy.Column(alchemy.Boolean)

    person_id = alchemy.Column(
        alchemy.Integer, alchemy.ForeignKey('person.id'))

    def __init__(self, date, target, remaining,  consumption, percentage, is_goal, person_id):
        self.date = date
        self.target = target
        self.remaining = remaining
        self.consumption = consumption
        self.percentage = percentage
        self.is_goal = is_goal
        self.person_id = person_id

    def json(self):
        return {
            'date': self.date,
            'target': self.target,
            'remaining': self.remaining,
            'consumption': self.consumption,
            'percentage': self.percentage,
            'is_goal': self.is_goal,
            'person_id': self.person_id
        }
    
    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()
        
    @classmethod
    def find_one_by_id(cls, id):
        cls.query.filter_by(id=id).first()
        
    @classmethod
    def find_all_by_id(cls, id):
        cls.query.filter_by(id=id)
