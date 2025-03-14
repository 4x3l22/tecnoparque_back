from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flaskr.apis.urls import api_blueprint

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# 🔹 Registrar los Blueprints
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
