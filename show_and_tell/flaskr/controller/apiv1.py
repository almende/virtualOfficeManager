from flask import Blueprint
from flask_restx import Api

from .apis.contacts import api as ns_contacts

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint,
          title='Show and tell manager',
          version='1.0',
          description='A tool to manage show-and-tells',
          # All API metadatas
          )

api.add_namespace(ns_contacts)
