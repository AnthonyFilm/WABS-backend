
# from models import User, db, check_password_hash
from flask import Blueprint, request, redirect, url_for, flash, jsonify, session
# from werkzeug.security import generate_password_hash, check_password_hash
# from helpers import createBucket

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# imports for flask login
# from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/')
def home():
    return "The API server for Write A Bad Song has sucessfully started!"

# *****************TURNED CONFIRMATION EMAIL OFF in supabase FOR TESTING PURPOSES*****************
@auth.route('/signup', methods = ['POST'])
def signup_api():
    try:
        if request.method == 'POST':
            email_entered = request.json["email"]
            password = request.json["password"]
            name = request.json["name"]
            genre = request.json["genre"]
            phone_number = request.json["phone_number"]
            location = request.json["location"]
            profile_pic_url = request.json["profile_pic_url"]

 
     

            # user_exists = User.query.filter_by(email=email).first() is not None
            # if user_exists:
            #     return jsonify({"error": "User with that email already exists. Please try again."}), 409
            
            print(name, email_entered, "this again")
            # , data={"name": name, "genre": genre, "phone_number": phone_number, "location": location}

            res = supabase.auth.sign_up({
                        'email': email_entered,
                        'password': password,
                })
            
            print(res.user.id, "\n")
            # print(supabase.auth.user(), "\n")
            if len(res.user.id) > 0:
                
                user = res.user.id
                print(f'this is the user id {user}')
                # session = res.session
                response = supabase.table('profile').insert({
                    'id': user,
                    'name': name,
                    'genre': genre,
                    'phone_number': phone_number,
                    'location': location,
                    'profile_pic_url': profile_pic_url}).execute()
                print("we got afer the insert profile")


            
            # user = User(email, first_name, last_name, password=password)

            # db.session.add(user)
            # db.session.commit()

            # createBucket(user.id)
            print("we got here")


            # flash(f'You have successfully created a user account {email}', 'User-created')
            return user
   
    except Exception as e:
       
       return jsonify({'message': f'There is a problem with your sign up information. {type(e).__name__}: ${e}'}), 401
    return signup_api

@auth.route('/signin', methods = ['GET', 'POST'])
def signin(): 
    try:
        if request.method == 'POST':
            email = request.json["email"]
            password = request.json["password"]
            print(email)
            supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            # logged_user = User.query.filter(User.email == email).first()
          
            # if check_password_hash(logged_user.password, password):

                # login_user(logged_user)
                
                # session["user_id"] = logged_user.id
                
                # user_id = session.get("user_id")
            # print("this is the user id", user_id)
            return "success"
            # else:
            #     return jsonify({'message': 'There is a problem with your login information.'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'There is a problem with your login information.'}), 401
    return "something went wrong with the login process. Please try again."    

#  API route to verify login for React client

# @auth.route('/isauthenticated', methods=['POST'])
# @login_required
# def isauthenticated():
#     return session.get("user_id")

# # logout route 

# @auth.route('/logout')
# @login_required
# def logout():
#     session.pop("user_id")
#     logout_user()
#     return "You have successfully logged out"