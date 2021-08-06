from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from .models import FoodModel, PreparedModel
from . import serializers as srl
from datetime import datetime, timedelta, date
from flask_apispec import use_kwargs, doc, views



class PrepareFood(views.MethodResource, Resource): # Preparar comida

    parser = reqparse.RequestParser()
    parser.add_argument('food_id', type=int, required=True, help='No es formato entero')
    #parser.add_argument('expire', type=lambda x: datetime.strptime(x,'%Y-%m-%d'), required=True, help='No es una fecha')

    @doc(tags=['Comidas'], description='Cualquier usuario puede preparar alguna comida que esta en el modelo de comidas')
    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @use_kwargs(srl.PrepareRequest, location= ('json')) 
    @jwt_required()
    def post(self, **kwargs):
        
        data = PrepareFood.parser.parse_args()
        user = current_identity
        
        food = FoodModel.query.get(data['food_id']) # existe esa comida en la tabla
        if food is None:
            return {'message': 'No existe esa comida para poder prepararla'}, 400
        
        data['expire'] = date.today() + timedelta(days=food.expire) # Fecha de caducidad
        data['user_id'] = user.id

        pet = PreparedModel(**data)
        pet.save_to_db()

        return {"message": "La comida ha sido preparada satisfactoriamente"}


    @doc(tags=['Comidas'], description='Ver todas las comidas preparadas por todos los usuarios')
    def get(self): # Muestra info de las comidas preparadas

        foods = PreparedModel.query.all()
        result = srl.prepared_schema.dump(foods)
        
        return result



class NewFood(views.MethodResource, Resource): # Gestionar comidas que se pueden preparar
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='No es formato string')
    parser.add_argument('expire', type=int, required=True, help='No es formato entero')
    
    @doc(tags=['Comidas'], description='El admin puede aperturar nuevas comidas, para que los usuarios las preparen')
    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @use_kwargs(srl.FoodsRequest, location= ('json')) 
    @jwt_required()
    def post(self, **kwargs):
        
        data = NewFood.parser.parse_args()
        user = current_identity

        if user.id != 1: # el administrador tiene id 1
            return {"message": "No eres administrador para crear una nueva comida"}

        if FoodModel.query.filter_by(name = data['name']).first():
            return {'message': 'Ya existe esa comida'}, 400
        
        food = FoodModel(**data)
        food.save_to_db()

        return {"message": "Se creo una nueva comida satisfactoriamente"}
    
    @doc(tags=['Comidas'], description='Se visualizara todos las comidas que se pueden preparar')
    def get(self):

        foods = FoodModel.query.all()
        result = srl.foods_schema.dump(foods)

        return result

    




    