# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from flask_login import LoginManager
# from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
# login_manager = LoginManager()
# ma = Marshmallow()
# db = SQLAlchemy()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

# # 
# class User(db.Model, UserMixin):
#     id = db.Column(db.String, primary_key=True)
#     first_name = db.Column(db.String(150), nullable=True, default='')
#     last_name = db.Column(db.String(150), nullable = True, default = '')
#     email = db.Column(db.String(150), nullable = False)
#     password = db.Column(db.String, nullable = True, default = '')
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

#     def __init__ (self, email, first_name='', last_name='', password=''):
#         self.id = self.set_id()
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.password = self.set_password(password)

#     def set_id(self):
#         return str(uuid.uuid4())
    
#     def set_password(self, password):
#         self.pw_hash = generate_password_hash(password)
#         return self.pw_hash
    
#     def __repr__(self):
#         return f'User {self.email} has been added to the database'
    
# class Memory(db.Model):
#     id = db.Column(db.String, primary_key = True)
#     mem_title = db.Column(db.String(100), nullable=False)
#     family = db.Column(db.String(100), nullable=False)
#     share_votes = db.Column(db.Integer, default=0)
#     sharable = db.Column(db.Boolean, default=False)
#     mem_date = db.Column(db.Date, nullable=False) # if none must enter 'null'
#     medium = db.Column(db.String(100), nullable=False)
#     file_loc = db.Column(db.String, nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False) 

#     def __init__(self, mem_title, family, share_votes, sharable, medium, file_loc, mem_date="",description="", user_id="", id =''):
#         self.id = self.set_id()
#         self.mem_title = mem_title
#         self.family = family
#         self.share_votes = share_votes
#         self.sharable = sharable
#         self.mem_date = mem_date
#         self.medium = medium
#         self.file_loc = file_loc
#         self.description = description
#         self.user_id = user_id

#     def __rep__(self):
#         return f'The following memory has been added to your collection: a {self.medium} on {self.mem_date}'
    
#     def set_id(self):
#         return(secrets.token_urlsafe())

# class MemorySchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'mem_title', 'family', 'share_votes', 'sharable', 'mem_date', 'medium', 'file_loc', 'description', 'user_id']

# memory_schema = MemorySchema()
# memories_schema = MemorySchema(many=True)

# class Person(db.Model):
#     id = db.Column(db.String, primary_key = True)
#     person_first = db.Column(db.String(150), nullable=False)
#     person_last = db.Column(db.String(150), nullable=False)
#     person_middle = db.Column(db.String)
#     person_other = db.Column(db.String)
#     dob = db.Column(db.Date) # date of birth in string 'YYYY-MM-DD'
#     dod = db.Column(db.Date, nullable=True) # date of death in string 'YYYY-MM-DD', if none must enter 'null'
#     description = db.Column(db.Text, nullable=True)
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False) 

#     def __init__(self, person_first, person_last, dob, user_id, dod="", person_middle="", person_other="", description="",  id =''):
#         self.id = self.set_id()
#         self.person_first = person_first
#         self.person_last = person_last
#         self.person_middle = person_middle
#         self.person_other = person_other
#         self.dob = dob
#         self.dod = dod
#         self.description = description
#         self.user_id = user_id

#     def __rep__(self):
#         return f'The following person has been added: {self.person_first} {self.person_last}'
    
#     def set_id(self):
#         return(secrets.token_urlsafe())

# class PersonSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'person_first', 'person_last', 'person_middle', 'person_other', 'dob', 'dod', 'description']

# person_schema = PersonSchema()
# persons_schema = PersonSchema(many=True)

# class Connection(db.Model):
#     id = db.Column(db.String, primary_key = True)
#     person_id = db.Column(db.String, db.ForeignKey('person.id'), nullable=False)
#     memory_id = db.Column(db.String, db.ForeignKey('memory.id'), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     user_id= db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

#     def __init__(self, person_id, memory_id, description, user_id, id =''):
#         self.id = self.set_id()
#         self.person_id = person_id
#         self.memory_id = memory_id
#         self.description = description
#         self.user_id = user_id

#     def __rep__(self):
#         return f'The following connection has been added to your memories: person id {self.person_id} and memory id {self.memory_id}'
    
#     def set_id(self):
#         return(secrets.token_urlsafe())

# class ConnectionSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'person_id', 'memory_id', 'description']

# connection_schema = ConnectionSchema()
# connections_schema = ConnectionSchema(many=True)