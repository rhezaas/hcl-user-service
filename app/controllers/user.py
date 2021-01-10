from models.controller import ControllerModel
from models.middleware import Middleware
from models.query import QueryModel
from entities import User, Image
from flask import request


class UserController(ControllerModel):
    def routes(self):
        return {
            '/user': {
                'get': self.getMe,
                'put': self.updateUser
            },
            '/user/image': {
                'post': self.uploadImage
            }
        }

    @Middleware.authentication
    def getMe(self, user, transaction):
        _user = transaction.query(User)\
            .join(Image, Image.user_id == User.id, isouter=True)\
            .filter(User.id == user['id'])\
            .first()

        return {
            'id': _user.id,
            'firstname': _user.firstname,
            'lastname': _user.lastname,
            'phone': _user.phone,
            'image': list(map(lambda asset: {
                'id': asset.id,
                'image': asset.image,
                'width': asset.width,
                'height': asset.height
            }, _user.assets))
        }

    @Middleware.authentication
    def updateUser(self, user, transaction):
        data = request.json

        # update user
        user = QueryModel().update(User)\
            .values(data).where(User.id == user['id'])\
            .returning(
                User.id,
                User.firstname,
                User.lastname,
                User.phone,
                User.profile
            ).execute(transaction)\
            .fetchone()

        return {
            'id': user[0],
            'firstname': user[1],
            'lastname': user[2],
            'phone': user[3],
            'profile': user[4]
        }

    @Middleware.authentication
    def uploadImage(self, user, transaction):
        data = request.json

        image = QueryModel().insert(Image)\
            .values({
                'image': data['image'],
                'height': data['height'],
                'width': data['width'],
                'user_id': user['id']
            })\
            .returning(
                Image.id,
                Image.image,
                Image.height,
                Image.width,
            ).execute(transaction)\
            .fetchone()

        return {
            'id': image[0],
            'image': image[1],
            'height': image[2],
            'width': image[3]
        }
