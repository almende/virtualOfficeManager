from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
import pymongo
import bson

app = Flask(__name__, instance_relative_config=True)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Setup API
blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Funding API',
          description='An API to store funding opportunities',
          )
ns = Namespace('projects', description='Projects endpoints')
api.add_namespace(ns)
app.register_blueprint(blueprint, url_prefix='/api/v1')

# Setup mongodb
client = pymongo.MongoClient()
db = client['funding']

class ObjectId(fields.String):
    def format(self, value):
        bson.objectid.ObjectId(value)  # Upon failure: input is not a valid ObjectID and an exception will be raised
        return str(value)


project = api.model('Project', {
    '_id': ObjectId(readonly=True, description='Unique identifier'),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
})


obj_name = "project"


class FundingDAO(object):

    def read_all(self):
        return list(db.projects.find({}))

    def read(self, uid):
        return db.projects.find_one({"_id": bson.objectid.ObjectId(uid)})

    def create(self, data):
        inserted = db.projects.insert_one(data)
        return self.read(inserted.inserted_id)

    def update(self, uid, data):
        db.projects.update_one({"_id": bson.objectid.ObjectId(uid)}, {"$set": data})
        return self.read(uid)

    def delete(self, uid):
        deleted = db.projects.delete_one({"_id": bson.objectid.ObjectId(uid)})
        return deleted.deleted_count


DAO = FundingDAO()


@ns.route('/')
class ProjectList(Resource):
    '''Shows a list of all funding projects, and lets you POST to add new tasks'''

    @ns.doc('list_projects')
    @ns.marshal_list_with(project)
    def get(self):
        '''List all projects'''
        return DAO.read_all()

    @ns.doc('create_project')
    @ns.expect(project)
    @ns.marshal_with(project, code=201)
    def post(self):
        '''Create a new project'''
        return DAO.create(api.payload), 201


@ns.route('/<string:id>')
@ns.param('id', 'Unique identifier')
class Project(Resource):
    '''Manages a single project'''

    @ns.doc('get_project')
    @ns.marshal_with(project)
    @ns.response(404, '{} not found'.format(obj_name))
    @ns.response(200, '{} added'.format(obj_name))
    def get(self, id):
        '''Fetch a given resource'''
        try:
            return DAO.read(id)
        except:
            api.abort(404, "{} {} not found".format(obj_name, id))

    @ns.doc('delete_project')
    @ns.response(204, '{} deleted'.format(obj_name))
    @ns.response(404, '{} not found'.format(obj_name))
    def delete(self, id):
        '''Delete a task given its identifier'''
        try:
            r = DAO.delete(id)
        except:
            r = 0
        finally:
            if r > 0:
                return '', 204
            else:
                api.abort(404, "{} {} not found".format(obj_name, id))

    @ns.expect(project)
    @ns.marshal_with(project)
    @ns.response(204, '{} updated'.format(obj_name))
    @ns.response(404, '{} not found'.format(obj_name))
    def put(self, id):
        '''Update a task given its identifier'''
        try:
            return DAO.update(id, api.payload)
        except:
            api.abort(404, "{} {} not found".format(obj_name, id))


if __name__ == '__main__':
    app.run(debug=True)
