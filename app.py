
from src.settings import app, db
from src.users.security import identity, authenticate

from flask_jwt import JWT


db.init_app(app)
jwt = JWT(app, authenticate, identity)


if __name__=='__main__':
    app.run()
