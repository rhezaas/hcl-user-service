from flask import request
from entities import Account, User
from models.error import UnauthorizedException
from inspect import getargspec


class Middleware:
    @staticmethod
    def authentication(function):
        def wrapper(self, transaction):
            token = request.headers['Authorization'].split(' ')[1]

            user = transaction.select(User)\
                .join(Account, Account.user_id == User.id)\
                .filter(Account.token == token)\
                .first()

            if not (user is None):
                if 'transaction' in getargspec(function)[0]:
                    if 'user' in getargspec(function)[0]:
                        return function(self, {
                            'id': user.id,
                            'firstname': user.firstname,
                            'lastname': user.lastname,
                            'phone': user.phone,
                        }, transaction)
                    else:
                        return function(self, transaction)
                else:
                    if 'user' in getargspec(function)[0]:
                        return function(self, {
                            'id': user.id,
                            'firstname': user.firstname,
                            'lastname': user.lastname,
                            'phone': user.phone,
                        })
                    else:
                        return function(self)
            else:
                raise UnauthorizedException('')

        wrapper.__name__ = function.__name__
        return wrapper
