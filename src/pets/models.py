
from src.settings import db

food_pet = db.Table('foods_pets',
    db.Column('foods_id', db.Integer(), db.ForeignKey('foods.id'), primary_key=True),
    db.Column('pets_id', db.Integer(), db.ForeignKey('pets.id'), primary_key=True),
)

class PetModel(db.Model): # modelo mascota

    __tablename__ = 'pets' # tabla mascotas

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    health = db.Column(db.Integer, default=50) # Salud de la mascota
    favorite_food = db.Column(db.String(100)) # Comida favorita
    dream_state = db.Column(db.Integer, default=50) # Estado de sueño

    # Relaciones one to many
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel', backref=db.backref('pet_user', lazy=True))

    specie_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    specie = db.relationship('SpecieModel', backref=db.backref('pet_specie', lazy=True))

    # Relaciones many to many
    foods = db.relationship('FoodModel', secondary=food_pet, backref=db.backref('pets_food', lazy='dynamic'))


    def __init__(self, name, favorite_food, specie_id, user_id):
        self.name = name
        self.favorite_food = favorite_food
        self.specie_id = specie_id
        self.user_id = user_id
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_db(self):
        db.session.commit()
    
    def delete_pet(self):
        db.session.delete()
        db.commit()

    def __repr__(self):
        return f'Pet {self.name}'
    

class SpecieModel(db.Model): # modelo para especies de mascotas

    __tablename__ = 'species' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'