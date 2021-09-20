#!/usr/bin/python3
"""Users"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False, methods=['GET', 'POST'])
def places_by_city_id(city_id):
    '''Retrieves the list of all Place objects of a City'''
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if request.method == 'GET':
        places_list = [place.to_dict() for place in city.places]
        return jsonify(places_list)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        if 'user_id' not in data.keys():
            abort(400, description='Missing user_id')

        if 'name' not in data.keys():
            abort(400, description='Missing name')

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route(
    '/places/<place_id>', strict_slashes=False,
    methods=['GET', 'DELETE', 'PUT'])
def place_by_id(place_id):
    '''Retrieves a City object'''

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        attributes_to_ignore = [
            'id', 'user_id', 'city_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in attributes_to_ignore:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
