
from models import User, db, check_password_hash
from flask import Blueprint, request, redirect, url_for, flash, jsonify, session
from helpers import createBucket


# imports for flask login
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/')
def home():
    return "The API server for Family Function has sucessfully started!"


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            email = request.json["email"]
            password = request.json["password"]
            first_name = request.json["first_name"]
            last_name = request.json["last_name"]

            user_exists = User.query.filter_by(email=email).first() is not None
            if user_exists:
                return jsonify({"error": "User with that email already exists. Please try again."}), 409
            
            print(first_name, last_name, email)

            user = User(email, first_name, last_name, password = password)

            db.session.add(user)
            db.session.commit()

            createBucket(user.id)



            flash(f'You have successfully created a user account {email}', 'User-created')
            return jsonify({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "id": user.id,
                "email": user.email
            })
   
    except:
       return jsonify({'message': 'There is a problem with your login information.'}), 401
    return signup

@auth.route('/signin', methods = ['GET', 'POST'])
def signin(): 
    try:
        if request.method == 'POST':
            email = request.json["email"]
            password = request.json["password"]
            print(email)

            logged_user = User.query.filter(User.email == email).first()
          
            if logged_user and check_password_hash(logged_user.password, password):

                login_user(logged_user)
                
                session["user_id"] = logged_user.id
                
                user_id = session.get("user_id")
                print("this is the user id", user_id)
                return jsonify({'user_id': user_id, 'message': 'auth-success'})
            else:
                return jsonify({'message': 'There is a problem with your login information.'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'There is a problem with your login information.'}), 401
    return "something went wrong with the login process. Please try again."    

#  API route to verify login for React client

@auth.route('/isauthenticated', methods=['POST'])
@login_required
def isauthenticated():
    return session.get("user_id")

# logout route 

@auth.route('/logout')
@login_required
def logout():
    session.pop("user_id")
    logout_user()
    return "You have successfully logged out"