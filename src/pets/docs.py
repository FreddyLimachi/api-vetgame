from src.settings import docs
from . import views


# Registrar Apis para swagger
docs.register(views.NewSpecie)
docs.register(views.NewPet)
docs.register(views.FeedPet)
docs.register(views.SayHello)
docs.register(views.PlayPet)
docs.register(views.SleepPet)