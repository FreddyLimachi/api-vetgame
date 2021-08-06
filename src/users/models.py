
from src.settings import db, bcrypt

class UserModel(db.Model): # Modelo usuarios

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    
    health = db.Column(db.Integer, default=50) #salud del usuario inicia en 50
    dream_state = db.Column(db.Integer, default=50) # Estado de sueño del usuario inicia en 50

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_db(self):
        db.session.commit()
    
    def __repr__(self):
        return f'user {self.username}'



    