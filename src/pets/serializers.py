from src.settings import ma
from marshmallow import fields

class AuthRequest(ma.Schema):
    Authorization = fields.Str(
            required=True,
            description= 'Autorizacion HTTP header con JWT'
        )

class FoodsLikeSchema(ma.Schema):
    id = fields.Int(description="Id de la comida que come la mascota")


class PetsRequest(ma.Schema):
    name = fields.String(required=True, description="Nombre de la mascota")
    favorite_food = fields.String(required=True, description="comida favorita de la mascota")
    specie_id = fields.Integer(required=True, description="id de la especie de la mascota")
    foods_id =  fields.List(fields.Nested(FoodsLikeSchema), description="id de las comidas que come la mascota")

class SpecieRequest(ma.Schema):
    name = fields.String(required=True, description="Nombre de la especie")


class FeedPetRequest(ma.Schema):
    pet_id = fields.Integer(required=True, description="id de la mascota que quiere alimentar")
    food_id = fields.Integer(required=True, description="id de la comida que quiere darle a la mascota")


class PlayPetRequest(ma.Schema):
    my_pet_id = fields.Integer(required=True, description="id de tu mascota")
    other_pet_id = fields.Integer(required=True, description="id de la otra mascota")
    

class SpeciesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class FoodsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class PetsSchema(ma.Schema):
    foods = fields.Nested(FoodsSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'health','favorite_food', 'dream_state', 'foods', 'user.id')


species_schema = SpeciesSchema(many=True)
pets_schema = PetsSchema(many=True)
