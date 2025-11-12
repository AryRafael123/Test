from sqlalchemy.exc import IntegrityError
from flask import Blueprint, Flask, app, render_template, request, redirect, url_for, jsonify, current_app
from flask import session
from flask_login import login_user, current_user
import jwt
import datetime

main = Blueprint('main', __name__)



@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST': 
        print("Form submitted")
        from .services import authenticate_user
        username_form = request.form.get('username')
        password_form = request.form.get('password')
        user_data = authenticate_user(username_form, password_form)

        if user_data[1] == True:
            token = jwt.encode({
                'sub': username_form,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')
            response = redirect("http://localhost/dashboard")
            response.set_cookie("access_token", token, httponly=True)
            return response
            
            
        
        return jsonify({'error': 'Invalid credentials'}), 401

    return render_template("login.html")



@main.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        from .services import create_user
        if create_user(
            google_id=None,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            username=request.form.get('username'),
            email=request.form.get('email'),
            image= None,  # Default image will be set in the service
            OAuthx= False  # OAuth is not used in this case
        ):
            return render_template('login.html')
        
    return render_template('signup.html')