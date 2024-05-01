import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from supabase import create_client, Client
from flask_uploads import UploadSet, configure_uploads, IMAGES

# Supabase Configuration
SUPABASE_URL = 'your_supabase_url'
SUPABASE_KEY = 'your_supabase_anon_key'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flask Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'  # Folder to store photos
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# ... your other Flask app logic ...

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        genre = request.form['genre']
        location = request.form['location']
        password = request.form['password']

        # Profile photo handling
        if 'profile_photo' in request.files:
            photo = request.files['profile_photo']
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))

            # Upload to Supabase Storage
            upload_result = supabase.storage().from_('your_bucket_name').upload(filename, os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            profile_photo_url = supabase.storage().from_('your_bucket_name').get_public_url(filename)

        # Sign up the user
        user = supabase.auth.sign_up({'email': email, 'password': password} data={
            'name': name,
            'phone_number': phone_number,
            'genre': genre,
            'location': location,
            'profile_photo_url': profile_photo_url if profile_photo_url else None,
        })
        if user:
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))  # Replace 'login' with your login route
        else:
            flash('Signup failed. Please try again.', 'error')

    return render_template('signup.html')  # Replace 'signup.html' with your template