#!/usr/bin/python3
""" Blueprint for city objs that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def city(city_id=None, state_id=None):
    """ Retrieves City obj """
    state_objects = storage.get("State", state_id)
    if city_id is None and state_objects is not None:
        cities = storage.all("City")
        my_cities = [value.to_dict() for key, value in cities.items()]
        return jsonify(my_cities)

    my_cities = storage.get("City", city_id)
    if my_cities is not None:
        return jsonify(my_cities.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_cities(city_id):
    """ Deletes a city obj based on its' id """

    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)
    storage.delete(my_city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=["POST"], strict_slashes=False)
def cities_by_state(state_id=None):
    """gets the cities by state"""
    content = request.get_json()
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    my_name = content.get("name")
    if my_name is None:
        return (jsonify({"error": "Missing name"}), 400)
    new_city = City(**content)
    new_city.state_id = state_id
    new_city.save()

    return(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods=["POST"], strict_slashes=False)
@app_views.route('/cities', methods=["POST"], strict_slashes=False)
def post_cities(city_id=None):
    """ Creates a City """
    content = request.get_json()
    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_city = City(**content)
    new_city.save()

    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_cities(city_id):
    """ Updates a City obj & id """
    content = request.get_json()
    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_city, key, value)

    my_city.save()
    return jsonify(my_city.to_dict(), 200)
