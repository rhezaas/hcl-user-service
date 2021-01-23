from models import ControllerModel, Middleware
from entities import Profile, Image
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
        images = transaction.select(Image)\
            .filter(Image.profile_id == user['profile_id'])\
            .all()

        return {
            'account_id': user['account_id'],
            'profile_id': user['profile_id'],
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'phone': user['phone'],
            'image': list(map(lambda asset: {
                'id': asset.id,
                'image': asset.image,
                'width': asset.width,
                'height': asset.height
            }, images))
        }

    @Middleware.authentication
    def updateUser(self, user, transaction):
        data = request.json

        # update user
        user = transaction.update(Profile)\
            .values(data).where(Profile.id == user['profile_id'])\
            .returning(
                Profile.id,
                Profile.firstname,
                Profile.lastname,
                Profile.phone,
                Profile.profile
            ).execute()\
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

        image = transaction.insert(Image)\
            .values({
                'image': data['image'],
                'height': data['height'],
                'width': data['width'],
                'profile_id': user['profile_id']
            })\
            .returning(
                Image.id,
                Image.image,
                Image.height,
                Image.width,
            ).execute()\
            .fetchone()

        return {
            'id': image[0],
            'image': image[1],
            'height': image[2],
            'width': image[3]
        }
