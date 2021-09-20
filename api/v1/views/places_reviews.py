#!/usr/bin/python3
"""Places and reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False, methods=['GET', 'POST'])
def reviews_by_place_id(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews_list = [review.to_dict() for review in place.reviews]
        return jsonify(reviews_list)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        if 'user_id' not in data.keys():
            abort(400, description='Missing user_id')

        if 'text' not in data.keys():
            abort(400, description='Missing text')

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        data['place_id'] = place_id
        new_review = Review(**data)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>', strict_slashes=False,
    methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    '''Retrieves a Review object'''

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        attributes_to_ignore = [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in attributes_to_ignore:
                setattr(review, key, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
