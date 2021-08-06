from src.settings import db

class FoodModel(db.Model): # comidas preparadas

    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    expire = db.Column(db.Integer, default=1, nullable = False) # En cuantos dias se pudre

    def __init__(self, name, expire):
        self.name = name
        self.expire = expire
    
    def __repr__(self):
        return f'Food {self.name}'
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class PreparedModel(db.Model): # tipos de comida

    __tablename__ = 'prepared' 

    id = db.Column(db.Integer, primary_key=True)
    expire = db.Column(db.Date, nullable=False)
    
    # relaciones
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    food = db.relationship('FoodModel', backref=db.backref('foods', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel', backref=db.backref('pets', lazy=True))


    def __init__(self, food_id, user_id, expire):
        self.food_id = food_id
        self.user_id = user_id
        self.expire = expire

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.food.name}'





