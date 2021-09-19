#!/usr/bin/python3
"""States"""

from api.v1.views import app_views
from flask import Flask, jsonify, redirect
from models import storage
from models.state import State
from api.v1.app import not_found


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    # objects dictionary
    states_dict = storage.all(State)
    #  Iterate -> to dict -> save in list
    states_list = [state.to_dict() for state in states_dict.values()]
    print(states_list)
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    return jsonify({"error": "Not found"}), 404

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404