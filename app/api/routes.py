from flask import Blueprint, request, jsonify, render_template, session
from flask_login import (
    current_user,
    login_required
)

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

from models import db, User, Memory, memory_schema, memories_schema, Person, person_schema, persons_schema, Connection, connection_schema, connections_schema

api = Blueprint('api',__name__, url_prefix='/api')



#  API routes for memories

@api.route('/memories', methods = ['POST'])
@login_required
def create_memory():
    print(f'first: {session.get("user_id")}')
    family = request.json['family']
    mem_title = request.json['mem_title']
    share_votes = request.json['share_votes']
    # sharable = request.json['sharable']
    mem_date = request.json['mem_date'] # must be a string in the form of 'yyyy-mm-dd'
    medium = request.json['medium']
    file_loc = request.json['file_loc']
    description = request.json['description']
    user_id = session.get("user_id")

    memory = Memory(mem_title=mem_title, family=family,sharable=False, share_votes=1, medium=medium, file_loc=file_loc, mem_date=mem_date, description=description, user_id=user_id, id ='')

    db.session.add(memory)
    db.session.commit()

    response = memory_schema.dump(memory)
    # return "hello"
    return jsonify(response)

@api.route('/memories', methods = ['GET'])
@login_required
def get_memory():
    a_user = session.get("user_id")
    memories = Memory.query.filter_by(user_id = a_user).all()
    response = memories_schema.dump(memories)
    return jsonify(response)

@api.route('/memories/<id>', methods = ['GET'])
@login_required
def get_single_memory(id):
    memory = Memory.query.get(id)
    response = memory_schema.dump(memory)
    return jsonify(response)

@api.route('/memories/<id>', methods = ['POST','PUT'])
@login_required
def update_memory(id):
    memory = Memory.query.get(id) 
    memory.family = request.json['family']
    memory.mem_title = request.json['mem_title']
    memory.share_votes = request.json['share_votes']
    memory.sharable = request.json['sharable']
    memory.mem_date = request.json['mem_date'] # must be a string in the form of 'yyyy-mm-dd'
    memory.medium = request.json['medium']
    memory.file_loc = request.json['file_loc']
    memory.description = request.json['description']
    memory.user_id = session.get("user_id")


    db.session.commit()
    response = memory_schema.dump(memory)
    return jsonify(response)

@api.route('/memories/<id>', methods = ['DELETE'])
@login_required
def delete_memory(id):
    memory = Memory.query.get(id)
    db.session.delete(memory)
    db.session.commit()
    response = memory_schema.dump(memory)
    return jsonify(response)


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
    
    response = supabase.from_('profile').select('*').eq('user_id', user_id).execute()
    return jsonify(response)

@api.route('/profile/<id>', methods = ['POST','PUT'])
@login_required
def update_person(id):
    person = Person.query.get(id) 
    person.person_first = request.json['person_first']
    person.person_last = request.json['person_last']
    person.person_middle = request.json['person_middle']
    person.person_other = request.json['person_other']
    person.dob = request.json['dob']
    person.dod = request.json['dod']
    person.description = request.json['description']
    person.user_id = session.get("user_id")

    db.session.commit()
    response = person_schema.dump(person)
    return jsonify(response)

@api.route('/persons/<id>', methods = ['DELETE'])
@login_required
def delete_person(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    response = person_schema.dump(person)
    return jsonify(response)

