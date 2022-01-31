from flask_cors import CORS
from app_routes import *
from starter import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

CORS(app, support_credentials=True)
mallow = Marshmallow(app)

if __name__ == '__main__':
    # * --- DEBUG MODE: --- *
    app.run(host='127.0.0.1', port=5000, debug=True)

