from flask import Blueprint
from flask_restx import Api
from .apis.projects import ns as ns_projects

# Setup API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='Funding API',
          description='An API to store funding opportunities',
          )


api.add_namespace(ns_projects)