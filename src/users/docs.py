from src.settings import docs
from . import views


# Registrar Apis para swagger
docs.register(views.UserRegister)
docs.register(views.FeedUser)
docs.register(views.SleepUser)