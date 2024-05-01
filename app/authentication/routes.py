
# from models import User, db, check_password_hash
from flask import Blueprint, request, redirect, url_for, flash, jsonify, session,json
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
            print('before')
            email_entered =request.form.get("email")
            password = request.form.get("password")
            name = request.form.get("name")
   
            genre = request.form.get("genre")
            phone_number = request.form.get("phone_number")
            location = request.form.get("location")
            print('after')
            

 
     

            # user_exists = User.query.filter_by(email=email).first() is not None
            # if user_exists:
            #     return jsonify({"error": "User with that email already exists. Please try again."}), 409
            
            print(name, email_entered, "this again")
            # , data={"name": name, "genre": genre, "phone_number": phone_number, "location": location}

            res = supabase.auth.sign_up({
                        'email': email_entered,
                        'password': password,
                })
            user_id = res.user.id
            print(user_id, "\n")
            # print(supabase.auth.user(), "\n")
            if len(res.user.id) > 0:
                if 'profile_pic' in request.files:
                    photo = request.files['profile_pic']
                    filename = res.user.id + photo.filename.replace(" ", "")  # Always sanitize filenames
                    filepath = os.path.join('/tmp', filename)
                    photo.save(filepath)
                    print('after file save')
                    # Directly upload to Supabase Storage
                    with open(filepath, 'rb') as f:
                        print(filepath)
                        print(f)
                        response = supabase.storage.from_('profile-pic').upload(file=f, path=filename, file_options={"content-type": "image/*"})
                        print(response)
                    # upload_result = supabase.storage().from_('profile-pic').upload(filename, photo)
                    print('after upload')
                    profile_pic_url = supabase.storage.from_('profile-pic').get_public_url(filename)
                    print(profile_pic_url)
                    print('after get public url')
                
                
                print(f'this is the user id {user_id}')
                # session = res.session
                response = supabase.table('profile').insert({
                    'id': user_id,
                    'name': name,
                    'genre': genre,
                    'phone_number': phone_number,
                    'location': location,
                    'profile_pic_url': profile_pic_url}).execute()
                print("we got afer the insert profile")

            print("we got here")
            return response.json()
   
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
            ret = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            user_id = ret.user.id

            print(user_id)
            # logged_user = User.query.filter(User.email == email).first()
          
            # if check_password_hash(logged_user.password, password):

                # login_user(logged_user)
                
                # session["user_id"] = logged_user.id
                
                # user_id = session.get("user_id")
            # print("this is the user id", user_id)
            return ret.json()
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