from waitress import serve
from flask import Flask
import controllers
from decouple import config


class Server():
    def __init__(self):
        self.__flask__ = Flask('User Service')

    def config(self):
        self.__flask__.route('/', methods=['GET'])(lambda: 'User service is running')  # noqa: E501

        self.__flask__.config['JSON_SORT_KEYS'] = False
        self.__flask__.config['ENV'] = config('ENV')

        return self

    def serveRoutes(self):
        for controller in controllers.__all__:
            controller(self.__flask__)

        return self

    def run(self):
        if config('ENV') == 'production':
            serve(self.__flask__)
        else:
            self.__flask__.run(port=config('PORT'))
