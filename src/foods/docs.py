from src.settings import docs
from . import views


# Registrar Apis para swagger
docs.register(views.NewFood)
docs.register(views.PrepareFood)

