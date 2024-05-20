import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from . import db, bcrypt
from .models import User, Log
from flask_login import login_user, login_required, current_user, logout_user
from .utils import detect_signature
import json

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.detect_signature_route'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))

@main.route('/detect_signature', methods=['GET', 'POST'])
@login_required
def detect_signature_route():
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            flash('No file provided', 'danger')
            return redirect(request.url)
        
        uploads_dir = './uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        image_path = os.path.join(uploads_dir, file.filename)
        file.save(image_path)
        
        signatures = detect_signature(image_path)
        formatted_signatures = [
            {
                "x": sig["x"],
                "y": sig["y"],
                "width": sig["width"],
                "height": sig["height"],
                "image_url": url_for('static', filename=sig["image_path"][2:], _external=True)  
            } for sig in signatures
        ]
        result = {
            "message": "Signature detection completed",
            "signatures_found": len(signatures),
            "signatures": formatted_signatures
        }
        
        log = Log(
            user_id=current_user.id,
            endpoint=request.path,
            request_data=json.dumps(request.form.to_dict()),
            response_data=json.dumps(result)
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(result), 200
    return render_template('detect_signature.html')
