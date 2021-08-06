
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from .models import UserModel
from .serializers import user_schema, UserRequest, AuthRequest
from flask_apispec.views import MethodResource
from flask_apispec import use_kwargs, doc



class UserRegister(MethodResource, Resource): # Registrar un usuario

    @doc(tags=['Usuarios'], description='Registrar usuario')
    @use_kwargs(UserRequest, location = ( 'json' )) 
    def post(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='No es formato string')
        parser.add_argument('password', type=str, required=True, help='No es formato string'
        )
        data = parser.parse_args()

        if UserModel.query.filter_by(username = data['username']).first():
            return {'message': 'Ya existe el nombre de usuario'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'Usuario registrado satisfactoriamente'}, 201
    

    @doc(tags=['Usuarios'], description='Obtener datos del usuario')
    @use_kwargs(AuthRequest, location= ('headers'))
    @jwt_required()
    def get(self, **kwargs): # Mostrar su información y sus mascotas
        user = current_identity
        return user_schema.jsonify(user)



@doc(tags=['Usuarios'], description='Alimentar usuario')
class FeedUser(MethodResource, Resource): # El usuario come
    
    @use_kwargs(AuthRequest, location= ('headers'))
    @jwt_required()
    def put(self, **kwargs): # Actualizar su estado de salud
        
        user = current_identity

        user.health += 25 #aumenta su salud
        user.update_db()

        return {"message": "Se le asigno +25 de salud"}



@doc(tags=['Usuarios'], description='Dormir usuario')
class SleepUser(MethodResource, Resource): # El usuario come

    @use_kwargs(AuthRequest, location= ('headers'))
    @jwt_required()
    def put(self, **kwargs): # Actualizar su estado de salud
        
        user = current_identity

        user.dream_state += 25 #aumenta su salud
        user.update_db()

        return {"message": "Se le asigno +25 de estado de sueño"}
    
