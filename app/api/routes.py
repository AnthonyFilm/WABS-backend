from flask import Blueprint, request, jsonify, render_template, session
# from flask_login import (
#     current_user,
#     login_required
# )

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


api = Blueprint('api',__name__, url_prefix='/api')






#  api routes for profile 



# @api.route('/profile', methods = ['GET'])
# @login_required
# def get_persons():
#     a_user = session.get("user_id")
#     persons = Person.query.filter_by(user_id = a_user).all()
#     response = persons_schema.dump(persons)
#     return jsonify(response)

@api.route('/profile/<id>', methods = ['GET'])
def get_single_person(id):
    response = supabase.table('profile').select('*').eq('id', id).execute()
    print(response)
    return response.json()

# @api.route('/profile/<id>', methods = ['POST','PUT'])
# @login_required
# def update_person(id):
#     person = Person.query.get(id) 
#     person.person_first = request.json['person_first']
#     person.person_last = request.json['person_last']
#     person.person_middle = request.json['person_middle']
#     person.person_other = request.json['person_other']
#     person.dob = request.json['dob']
#     person.dod = request.json['dod']
#     person.description = request.json['description']
#     person.user_id = session.get("user_id")

#     db.session.commit()
#     response = person_schema.dump(person)
#     return jsonify(response)

# @api.route('/persons/<id>', methods = ['DELETE'])
# @login_required
# def delete_person(id):
#     person = Person.query.get(id)
#     db.session.delete(person)
#     db.session.commit()
#     response = person_schema.dump(person)
#     return jsonify(response)

