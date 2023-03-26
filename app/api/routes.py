from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Soda, soda_schema, sodas_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/sodas', methods = ['POST'])
@token_required
def create_soda(current_user_token):
    name = request.json['name']
    country_of_origin = request.json['country_of_origin']
    flavor_profile = request.json['flavor_profile']
    description = request.json['description']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    soda = Soda(name, country_of_origin, flavor_profile, description, user_token = user_token )

    db.session.add(soda)
    db.session.commit()

    response = soda_schema.dump(soda)
    return jsonify(response)




@api.route('/sodas', methods = ['GET'])
@token_required
def get_sodas(current_user_token):
    a_user = current_user_token.token
    sodas = Soda.query.filter_by(user_token = a_user).all()
    response = sodas_schema.dump(sodas)
    return jsonify(response)

@api.route('/sodas/<id>', methods = ['GET'])
@token_required
def get_soda_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        soda = Soda.query.get(id)
        response = soda_schema.dump(soda)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/sodas/<id>', methods= ['POST', 'PUT'])
@token_required
def update_soda(current_user_token, id):
    soda = Soda.query.get(id)
    soda.name = request.json['name']
    soda.country_of_origin = request.json['country_of_origin']
    soda.flavor_profile = request.json['flavor_profile']
    soda.description = request.json['description']
    soda.user_token = current_user_token.token

    db.session.commit()
    response = soda_schema.dump(soda)
    return jsonify(response)

@api.route('/sodas/<id>', methods=['DELETE'])
@token_required
def delete_soda(current_user_token, id):
    soda = Soda.query.get(id)
    db.session.delete(soda)
    db.session.commit()
    response = soda_schema.dump(soda)
    return jsonify(response)


