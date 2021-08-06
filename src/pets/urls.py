from . import views
from src.settings import api


# registrar rutas
api.add_resource(views.NewPet, '/new_pet')
api.add_resource(views.SayHello, '/say_hello/<int:id>')
api.add_resource(views.NewSpecie, '/species')

api.add_resource(views.FeedPet, '/feed_pet')
api.add_resource(views.SleepPet, '/sleep_pet/<int:id>')
api.add_resource(views.PlayPet, '/play_pet')

