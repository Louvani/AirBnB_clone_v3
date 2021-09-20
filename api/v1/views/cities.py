#!/usr/bin/python3
"""Cities"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City

@app_views.route(
    '/states/<state_id>/cities', strict_slashes=False, methods=['GET', 'POST'])
def cities_by_state_id(state_id):
    '''Retrieves the list of all City objects of a State'''

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == 'GET':
        cities_list = [city.to_dict() for city in state.cities]
        return jsonify(cities_list)

    if request.method == 'POST':

        if not request.get_json():
            abort(400, description='Not a JSON')

        data = request.get_json()

        if 'name' not in data.keys():
            abort(400, description='Missing name')
        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()

        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route(
    '/cities/<city_id>', strict_slashes=False,
    methods=['GET', 'DELETE', 'PUT'])
def city_by_id(city_id):
    '''Retrieves a City object'''

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            abort(400, description='Not a JSON')

        attributes_to_ignore = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in attributes_to_ignore:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
