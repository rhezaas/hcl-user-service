from flask import request
from entities import Account, Profile
from models.error import UnauthorizedException
from inspect import getargspec


class Middleware:
    @staticmethod
    def authentication(function):
        def wrapper(self, transaction):
            token = request.headers['Authorization'].split(' ')[1]

            account = transaction.select(Account)\
                .join(Profile, Profile.account_id == Account.id)\
                .filter(Account.token == token)\
                .first()

            if not (account is None):
                if 'transaction' in getargspec(function)[0]:
                    if 'user' in getargspec(function)[0]:
                        return function(self, {
                            'account_id': account.id,
                            'profile_id': account.profile.id,
                            'firstname': account.profile.firstname,
                            'lastname': account.profile.lastname,
                            'phone': account.profile.phone,
                        }, transaction)
                    else:
                        return function(self, transaction)
                else:
                    if 'user' in getargspec(function)[0]:
                        return function(self, {
                            'account_id': account.id,
                            'profile_id': account.profile.id,
                            'firstname': account.profile.firstname,
                            'lastname': account.profile.lastname,
                            'phone': account.profile.phone,
                        })
                    else:
                        return function(self)
            else:
                raise UnauthorizedException('')

        wrapper.__name__ = function.__name__
        return wrapper
