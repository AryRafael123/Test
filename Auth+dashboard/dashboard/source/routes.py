import jwt
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, Flask, app, render_template, request, redirect, url_for, jsonify
from flask import session
from flask_login import login_user, current_user

main = Blueprint('main', __name__)


@app.route('/dashboard' ,methods=['GET'])
def dashboard():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
    
    from services import verify_token
    
    token = auth_header.split(' ')[1]
    user = verify_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    return jsonify({'message': f'Welcome {user["sub"]}! Here is your menu.'})