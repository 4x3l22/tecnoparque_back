from flask import Blueprint
from flask_restful import Api
from .controllers import SensorController, SensorDataController, SensorunoController

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(SensorController, '/proceso/documents/<string:collection>')
api.add_resource(SensorunoController, '/proceso/list_end/<string:collection>')
api.add_resource(SensorDataController, '/proceso/documents_by_date/datos/<string:collection>')