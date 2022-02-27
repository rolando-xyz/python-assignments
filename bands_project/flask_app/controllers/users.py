from flask import render_template, session,redirect, request,flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.band import Band



bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods = ['POST'])
def register():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            **request.form,
            "password" : pw_hash
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email/password','error')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid password','login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html",user=User.get_one(data),bands=Band.get_bands(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')