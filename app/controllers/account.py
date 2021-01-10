from models.controller import ControllerModel
from flask import request
from entities import Account, User
from models.error import NotFoundException, UnauthorizedException
from hmac import new as hmac
from hashlib import sha3_512, sha3_256, md5, sha256
from decouple import config
from time import time


class AccountController(ControllerModel):
    def routes(self):
        return {
            '/account/register': {
                'post': self.register
            },
            '/account/login': {
                'post': self.login
            },
            '/account/auth': {
                'post': self.getAuth
            }
        }

    # get auth
    def getAuth(self, transaction):
        token = request.headers['Authorization'].split(' ')[1]

        user = transaction.select(User)\
            .join(Account, Account.user_id == User.id)\
            .filter(Account.token == token)\
            .first()

        return {
            'id': user.id
        }

    # register
    def register(self, transaction):
        data = request.json

        # hash password
        password = self.__hashPassword(data['password'])
        token = sha256(password.encode()).hexdigest()

        # add user
        user = transaction.insert(User).values({
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'phone': data['phone']
        }).returning(User.id).execute().fetchone()

        # add account
        transaction.insert(Account).values({
            'username': data['username'],
            'password': password,
            'token': token,
            'user_id': user[0]
        }).execute()

        return {
            'firsname': data['firstname'],
            'lastname': data['lastname'],
            'phone': data['phone'],
            'token': token
        }

    # login
    def login(self, transaction):
        data = request.json

        # query user
        account = transaction.select(Account)\
            .join(User, User.id == Account.user_id)\
            .filter(Account.username == data['username'])\
            .first()

        if not (account is None):
            # check password
            if self.__validatePassword(data['password'], account.password):
                # create new token
                token = sha256(f'{account.password}{time()}'.encode())\
                    .hexdigest()
                # update token
                transaction.update(Account)\
                    .values({'token': token})\
                    .where(Account.username == data['username'])\
                    .execute()

                return {
                    'id': account.user.id,
                    'firstname': account.user.firstname,
                    'lastname': account.user.lastname,
                    'phone': account.user.phone,
                    'token': token
                }
            else:
                raise UnauthorizedException('Wrond Password!')
        else:
            raise NotFoundException('User not found')

    # =============================== PRIVATE ===============================
    def __hashPassword(self, password: str):
        secret = bytes(config('API_SECRET'), 'utf-8')

        _password = hmac(secret, bytes(password, 'utf-8'), sha3_512).hexdigest()  # noqa : E501
        _password = hmac(secret, bytes(_password, 'utf-8'), sha3_256).hexdigest()  # noqa : E501
        _password = md5(_password.encode()).hexdigest()

        return _password

    def __validatePassword(self, password: str, storedPassword: str):
        _password = self.__hashPassword(password)

        if _password == storedPassword:
            return True
        else:
            return False
