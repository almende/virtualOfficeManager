from flask_restx import Resource, Namespace, fields
import bson
from flaskr.db import get_db

obj_name = "project"
ns = Namespace('{}s'.format(obj_name), description='{} endpoints'.format(obj_name))


class ObjectId(fields.String):
    def format(self, value):
        bson.objectid.ObjectId(value)  # Upon failure: input is not a valid ObjectID and an exception will be raised
        return str(value)


project = ns.model('Project', {
    '_id': ObjectId(readonly=True, description='Unique identifier'),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
})


class ProjectDAO(object):

    def read_all(self):
        return list(get_db().projects.find({}))

    def read(self, uid):
        return get_db().projects.find_one({"_id": bson.objectid.ObjectId(uid)})

    def create(self, data):
        inserted = get_db().projects.insert_one(data)
        return self.read(inserted.inserted_id)

    def update(self, uid, data):
        get_db().projects.update_one({"_id": bson.objectid.ObjectId(uid)}, {"$set": data})
        return self.read(uid)

    def delete(self, uid):
        deleted = get_db().projects.delete_one({"_id": bson.objectid.ObjectId(uid)})
        return deleted.deleted_count


DAO = ProjectDAO()


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