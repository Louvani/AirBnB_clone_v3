#!/usr/bin/python3
"""Amenities"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def all_amenities():
    '''Retrieves the list of all Amenities objects'''

    if request.method == 'GET':
        amenities = storage.all(Amenity)
        amenities_list = [amenity.to_dict() for amenity in amenities.values()]
        return jsonify(amenities_list)

    if request.method == 'POST':

        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        if 'name' not in data.keys():
            abort(400, description='Missing name')

        new_amenity = Amenity(**data)
        new_amenity.save()

        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    '''Retrieves a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            abort(400, description='Not a JSON')

        attributes_to_ignore = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in attributes_to_ignore:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
