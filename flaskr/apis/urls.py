from flask import Blueprint
from flask_restful import Api
from .controllers import ProyectoPostGetController, ProyectoPutDeleteController, SensorController, SensorDataController, \
    SensorunoController, UsuarioLoginController, \
    VistasPostGetController, VistasPutController, UsuarioPostGetController, UsuarioPutController

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(SensorController, '/proceso/documents/<string:collection>')
api.add_resource(SensorunoController, '/proceso/list_end/<string:collection>')
api.add_resource(SensorDataController, '/proceso/documents_by_date/datos/<string:collection>')
api.add_resource(VistasPostGetController, "/vistas") 
api.add_resource(VistasPutController, "/vistas/<int:id_vista>", endpoint="vista_update")
api.add_resource(UsuarioPostGetController, "/usaurio")
api.add_resource(UsuarioPutController, "/usaurio/<int:id_usuario>", endpoint="usuario_update")
api.add_resource(UsuarioLoginController, "/login")
api.add_resource(ProyectoPostGetController, "/proyecto")
api.add_resource(ProyectoPutDeleteController, "/proyecto/<int:id_proyecto>", endpoint="proyecto_update")