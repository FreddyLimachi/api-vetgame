from src.settings import ma
from marshmallow import fields


class AuthRequest(ma.Schema):
    Authorization = fields.Str(
            required=True,
            description= 'Autorizacion HTTP header con JWT'
        )

class FoodsRequest(ma.Schema):
    name = fields.String(required=True, description="Nombre de una nueva comida que se apertura")
    expire = fields.Integer(required=True, description="Nro de dias en el que caduca")


class PrepareRequest(ma.Schema):
    food_id = fields.Integer(required=True, description="Id de la comida que se quiere preparar")


class FoodsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'expire')


class PreparedSchema(ma.Schema):
    class Meta:
        fields = ('id', 'food.name', 'expire', 'user.username')


foods_schema = FoodsSchema(many=True)
prepared_schema = PreparedSchema(many=True)

