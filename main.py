from flask import Flask

from routes.routes import client_routes, account_routes

app = Flask(__name__)

client_routes(app)
account_routes(app)

if __name__ == '__main__':
    app.run()