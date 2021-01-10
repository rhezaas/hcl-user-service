from database import Database
from flask import make_response
from inspect import getargspec
from models.error import ErrorModel
from models.query import QueryModel


class ControllerModel:
    def __init__(self, server):
        self.mapRoute(server)

    def routes(self) -> dict:
        pass

    def mapRoute(self, server):
        routes = self.routes()

        for route in routes:
            for method in routes[route]:
                server.route(route, methods=[method.upper()])(self.transaction(routes[route][method]))  # noqa: E501

    def transaction(self, function):
        def wrapper():
            if 'transaction' in getargspec(function)[0]:
                try:
                    db = Database()
                    transaction = db.transaction()
                    return function(QueryModel(transaction))
                except ErrorModel as e:
                    db.rollback()
                    return self.exception(e.__dict__)
                finally:
                    db.commit()
                    db.close()
            else:
                try:
                    return function()
                except ErrorModel as e:
                    return make_response(e, 502)

        wrapper.__name__ = function.__name__
        return wrapper

    def exception(self, error):
        return make_response(error, error['code'])  # noqa: E501
