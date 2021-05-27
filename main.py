from flask import Flask

from routes.routes import client_routes, account_routes

import logging

app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG, format = f'%(asctime)s %(levelname)s %(message)s')

client_routes(app)
account_routes(app)

if __name__ == '__main__':
    app.run()