from __future__ import print_function
import googleapiclient.discovery
from flaskr.google_tools.google_service import build_credentials

from flask_restx import Namespace, Resource

from flask import request

api = Namespace('contacts', description='Contact related operations')


AUTHORIZATION_SCOPE = 'https://www.googleapis.com/auth/user.organization.read'


def build_contacts_api_v3():
    credentials = build_credentials(AUTHORIZATION_SCOPE)
    return googleapiclient.discovery.build('people', 'v1', credentials=credentials)

class ContactDAO(object):
    def read_all(self):
        people_service = build_contacts_api_v3()

        connections = people_service.people().connections() \
            .list(resourceName='people/me', personFields="names,emailAddresses,coverPhotos")

        return [] if connections.body is None else connections.body

    # def create(self, data):
    #     inserted = get_db().contact.insert_one(data)
    #     return self.read(inserted.inserted_id)

    # def read(self, rid):
    #     try:
    #         rid = bson.objectid.ObjectId(rid)
    #     except:
    #         api.abort(404, "There was no contact with id = {}.".format(rid))  # malformed id's will never be found
    #
    #     obj = get_db().contact.find_one({"_id": rid})
    #     if obj is None:
    #         api.abort(404, "There was no contact with id = {}.".format(rid))
    #     else:
    #         return objectid_in_dict_object_to_string(obj)
    #
    # def update(self, rid, data):
    #     try:
    #         rid = bson.objectid.ObjectId(rid)
    #     except:
    #         api.abort(404, "There was no contact with id = {}.".format(rid))  # malformed id's will never be found
    #
    #     get_db().contact.update_one({"_id": rid}, {"$set": data})
    #     return self.read(rid)
    #
    # def delete(self, rid):
    #     try:
    #         rid = bson.objectid.ObjectId(rid)
    #     except:
    #         api.abort(404, "There was no contact with id = {}.".format(rid))  # malformed id's will never be found
    #
    #     deleted = get_db().contact.delete_one({"_id": rid})
    #     return deleted.deleted_count


DAO = ContactDAO()

contact = api.model('Contact', {
    # '_id': fields.String(readonly=True),
    # 'name': fields.String(required=True),
    # 'description': fields.String(),
    # 'compute': OneOfCompute(),
    # 'previous_transforms': fields.List(fields.Nested(transform))
})


@api.route('/')
class ContactList(Resource):
    @api.doc('list_contacts')
    @api.response(200, "Success", contact)
    def get(self):
        """List all contacts"""
        return DAO.read_all(), 200

    @api.doc('post_contact')
    @api.response(200, "Success", contact)
    @api.expect(contact)
    def post(self):
        """Add a contact"""
        data = request.get_json()
        return DAO.create(data), 200