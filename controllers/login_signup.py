from flask import current_app as app, request, session, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.model import db,User
from datetime import datetime

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user) # Store user in session
                print(current_user)
                return redirect(url_for('dashboard'))
            else:
                return 'Invalid Password!'
        else:
            return 'Not a Verified User...'  
           
    return redirect(url_for('dashboard'))


@app.route("/signup", methods = ['POST', 'GET'])
def signup(): 
    return render_template("signup.html" , success = "Registration successful! ")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conformpassword = request.form['conformpassword']
        full_name = request.form['fullname']
        qualification = request.form['qualification']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template('signup.html', alert="User Already Exists...")
        
        elif password != conformpassword:
            return render_template('signup.html', alert = "Password and Conform Password are not same...")

        else:
            new_user = User(username=username, password=hashed_password, full_name = full_name, qualification= qualification, dob= dob)
            db.session.add(new_user)
            db.session.commit()
            return render_template("signup.html" , success = "Registration successful! ")
        
    return render_template("signup.html")
    
@app.route('/logout' , methods = ['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
