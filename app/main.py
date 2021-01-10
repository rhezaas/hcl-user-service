from flask import Flask
import controllers


server = Flask('user-service')
server.config['JSON_SORT_KEYS'] = False

server.route('/', methods=['GET'])(lambda: 'User service is running')

for controller in controllers.__all__:
    controller(server)
