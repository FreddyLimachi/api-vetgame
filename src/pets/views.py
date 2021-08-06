from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from .models import PetModel, SpecieModel
from . import serializers as srl
from src.foods.models import FoodModel, PreparedModel

from datetime import date
from flask_apispec import use_kwargs, doc, views



class NewPet(views.MethodResource, Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='No es formato string')
    parser.add_argument('favorite_food', type=str, required=True, help='No es formato string')
    parser.add_argument('specie_id', type=int, required=True, help='No es formato entero')
    parser.add_argument('foods_id', type=dict,action='append', required=True, help='No es formato lista')
    
    @doc(tags=['Mascotas'], description='Se obtiene nueva mascota')
    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @use_kwargs(srl.PetsRequest, location= ('json')) 
    @jwt_required()
    def post(self, **kwargs):
        
        data = NewPet.parser.parse_args()
        user = current_identity
     
        if PetModel.query.filter_by(user_id = user.id, name = data['name']).first():
            return {'message': 'Ya tienes una mascota con ese nombre'}, 400
        if SpecieModel.query.get(data['specie_id']) is None:
            return {'message': 'No existe esa especie'}, 400
        
        pet = PetModel(data['name'], data['favorite_food'], data['specie_id'], user.id)
        pet.save_to_db()
     
        for food in data['foods_id']:
            f = FoodModel.query.get(food['id'])
            if f is None: return {"message": "no existe esa comida"}

            pet.foods.append(f)
            pet.update_db()

        return {"message": "Se obtuvo una nueva mascota satisfactoriamente"}
    

    @doc(tags=['Mascotas'], description='Se visualiza todas las mascotas del usuario')
    @use_kwargs(srl.AuthRequest, location= ('headers')) 
    @jwt_required()
    def get(self, **kwargs):   # EL usuario obtiene los nombres de cada una de sus mascotas
        user = current_identity
        pets = PetModel.query.filter_by(user_id = user.id)
        result = srl.pets_schema.dump(pets)

        return result



class NewSpecie(views.MethodResource, Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='No es formato string')
    
    @doc(tags=['Mascotas'], description='El admin puede aperturar nuevas especies')
    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @use_kwargs(srl.SpecieRequest, location= ('json')) 
    @jwt_required()
    def post(self, **kwargs):
        
        data = NewSpecie.parser.parse_args()
        user = current_identity

        if user.id != 1: # el administrador tiene id 1
            return {"message": "No eres administrador para crear una nueva especie"}

        if SpecieModel.query.filter_by(name = data['name']).first():
            return {'message': 'Ya existe esa especie'}, 400
        
        specie = SpecieModel(**data)
        specie.save_to_db()

        return {"message": "Se creo una nueva especie de mascota satisfactoriamente"}
    
    @doc(tags=['Mascotas'], description='Se visualiza las especies disponibles')
    def get(self):

        species = SpecieModel.query.all()
        result = srl.species_schema.dump(species)

        return result
        

@doc(tags=['Mascotas'], description='Se gestiona la alimentación de mascotas')
class FeedPet(views.MethodResource, Resource): # La mascota se alimenta

    parser = reqparse.RequestParser()
    parser.add_argument('pet_id', type=int, required=True, help='No es formato entero')
    parser.add_argument('food_id', type=int, required=True, help='No es formato entero')

    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @use_kwargs(srl.FeedPetRequest, location= ('json'))
    @jwt_required()
    def put(self, **kwargs): # Alimentar y actualizar su salud
        
        data = FeedPet.parser.parse_args()
        user = current_identity

        pet = PetModel.query.filter_by(user_id = user.id, id = data['pet_id']).first()
        if pet is None: return {"message": "No tienes una mascota con ese id"}
        
        foods_id = []
        for food in pet.foods: foods_id.append(food.id)
        if data['food_id'] not in foods_id: return {"message": "La mascota no comio, por que no le gusta esa comida"}
        
        food = PreparedModel.query.filter_by(user_id = user.id, food_id = data['food_id']).first()
        if food is None: return {"message": "No preparaste esa comida"}
        
        now = date.today()
        if now < food.expire: 
            pet.health += 70
            pet.update_db()
            return {"message": "Se le aumentó 70 de salud"}

        pet.health += -40
        pet.update_db()

        if pet.health <= 0: 
            pet.delete_pet()
            return {"message": "La mascota se murió, por llegar a 0 de vida"}

        return {"message": "Se le quitó 40 de salud, la comida estaba podrida"}



@doc(tags=['Mascotas'], description='La mascota puede saludar a su dueño')
class SayHello(views.MethodResource, Resource): # La mascota saluda

    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @jwt_required()
    def get(self, id, **kwargs):

        user = current_identity
        pet = PetModel.query.filter_by(user_id = user.id, id=id).first()

        if pet: return {"message": f'Hola soy {pet.name}, mi comida favorita es {pet.favorite_food}'}
        
        return {"message": f'No tienes una mascota con el id {id}'}



class PlayPet(views.MethodResource, Resource): # La mascota juega con otras mascotas

    parser = reqparse.RequestParser()
    parser.add_argument('my_pet_id', type=int, required=True, help='No es formato entero')
    parser.add_argument('other_pet_id', type=int, required=True, help='No es formato entero')

    @doc(tags=['Mascotas'], description='La mascota puede jugar con otra mascota')
    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @use_kwargs(srl.PlayPetRequest, location= ('json'))
    @jwt_required()
    def put(self, **kwargs):
        data = PlayPet.parser.parse_args()
        user = current_identity

        if data['my_pet_id'] == data['other_pet_id']: return {"message": "Son la misma mascota"}

        my_pet = PetModel.query.filter_by(user_id = user.id, id=data['my_pet_id']).first()
        if my_pet is None: return {"message": "No tienes una mascota con ese id"}
        
        other_pet = PetModel.query.filter_by(id=data['other_pet_id']).first()
        if other_pet is None: return {"message": "Nadie tiene una mascota con ese id"}
        
        if my_pet.specie.id != other_pet.specie.id: return {"message": "La mascota no puede jugar con la mascota seleccionada por que no es su especie"}

        return {"message": "La mascota jugó satisfactoriamente"}
    

    @doc(tags=['Mascotas'], description='Se visualiza todas las mascotas de todos los usuarios')
    def get(self):
        pets = PetModel.query.all()
        result = srl.pets_schema.dump(pets)

        return result


@doc(tags=['Mascotas'], description='La mascota puede dormir para sumar su estado de sueño')
class SleepPet(views.MethodResource, Resource): # La mascota duerme

    @use_kwargs(srl.AuthRequest, location= ('headers'))
    @jwt_required()
    def put(self, id, **kwargs): # Actualizar su estado de sueño
        
        user = current_identity

        pet = PetModel.query.filter_by(user_id = user.id, id = id).first()
        if pet is None: return {"message": "No tienes una mascota con ese id"}
        
        pet.dream_state += 25 #aumenta su estado de sueño en 25
        pet.update_db()

        return {"message": "Se le asigno +25 de estado de sueño"}



