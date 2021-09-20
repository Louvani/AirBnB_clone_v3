#!/usr/bin/python3
"""States"""
from api.v1.views import app_views
from flask import Flask, jsonify, redirect, request, abort
from models import storage
from models.state import State
from api.v1.app import not_found


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    if request.method == 'GET':
        # objects dictionary
        states_dict = storage.all(State)
        #  Iterate -> to dict -> save in list
        states_list = [state.to_dict() for state in states_dict.values()]
        print(states_list)
        return jsonify(states_list)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, description='Not a JSON')
        data = request.get_json()
        if 'name' not in data.keys():
            abort(400, description='Missing name')
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route(
    '/states/<state_id>',
    strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is not None:
            return jsonify(state.to_dict())
        abort(404)
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is not None:
            storage.delete(state)
            # storage.save()
            return jsonify({}), 200
        abort(404)
    if request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if not request.get_json():
            abort(400, description='Not a JSON')
        data = request.get_json()
        attributes_to_ignore = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in attributes_to_ignore:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
