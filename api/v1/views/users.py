#!/usr/bin/python3
"""Users"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def all_users():
    '''Retrieves the list of all users objects'''

    if request.method == 'GET':
        users = storage.all(User)
        users_list = [user.to_dict() for user in users.values()]
        return jsonify(users_list)

    if request.method == 'POST':

        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        if 'email' not in data.keys():
            abort(400, description='Missing email')
        if 'password' not in data.keys():
            abort(400, description='Missing password')

        new_user = User(**data)
        new_user.save()

        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def users_by_id(user_id):
    '''Retrieves a user object'''
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            abort(400, description='Not a JSON')

        attributes_to_ignore = ['id', 'email', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in attributes_to_ignore:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
