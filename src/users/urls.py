from . import views
from src.settings import api

# registrar rutas
api.add_resource(views.UserRegister, '/register')
api.add_resource(views.FeedUser, '/feed_user')
api.add_resource(views.SleepUser, '/sleep_user')
