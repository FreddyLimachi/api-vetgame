from src.settings import ma
from marshmallow import fields


class AuthRequest(ma.Schema):
      
    Authorization = fields.Str(
            required=True,
            description= 'Autorizacion HTTP header con JWT'
        )
    
class UserRequest(ma.Schema):
    username = fields.String(required = True , description = "Nombre de usuario")
    password = fields.String(required = True , description = "Contraseña")


class PetsSchema(ma.Schema):
    class Meta:
        fields = ('id','name')

class UsersSchema(ma.Schema):
    pet_user = fields.Nested(PetsSchema, many=True)
    class Meta:
        fields = ('id', 'username', 'health', 'dream_state', 'pet_user')


user_schema = UsersSchema()

