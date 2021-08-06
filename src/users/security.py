from .models import UserModel, bcrypt


def authenticate(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if user and  bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.query.get(user_id)

