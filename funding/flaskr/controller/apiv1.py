from flask import Blueprint
from flask_restx import Api
from .apis.projects import ns as ns_projects
import os 
from flask import url_for


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

# Required to fix proxy issue to swagger.json
if os.environ.get('HTTPS_PROXY'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    Api.specs_url = specs_url

# Setup API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='Funding API',
          description='An API to store funding opportunities',
          security='API Key', authorizations=authorizations
          )


api.add_namespace(ns_projects)
