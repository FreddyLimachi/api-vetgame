from src.settings import api
from . import views

# registrar rutas

api.add_resource(views.PrepareFood, '/prepare_food')
api.add_resource(views.NewFood, '/foods')

