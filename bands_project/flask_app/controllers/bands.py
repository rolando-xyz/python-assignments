from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.band import Band


@app.route("/mybands")
def my_bands():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    return render_template("mybands.html",users=Band.get_bands(data),user=user)

@app.route("/new")
def add_band():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    return render_template("new_band.html",users=Band.get_bands(data),user=user)

@app.route('/add/new',methods=['POST'])
def post_band():
    if 'user_id' not in session:
        return redirect('/')
    if not Band.validate_band(request.form):
        return redirect('/new')
    data = {
            **request.form,
            'founder_id':session['user_id'],
            'founded_by':session['user_id']
        }
    Band.save_band(data)
    return redirect('/dashboard')


@app.route('/destroy/band/<int:id>')
def destroy_band(id):
    data = {
        "id": id
    }
    Band.destroy(data)
    return redirect('/dashboard')

@app.route("/edit/<int:id>")
def edit_band(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    user = User.get_one(data)
    return render_template("edit_band.html",band=Band.get_band(data),users=Band.get_bands(data),user=user)

@app.route('/band/update',methods=['POST'])
def update_band():
    if 'user_id' not in session:
        return redirect('/')
    if not Band.validate_band(request.form):
        return redirect('/new')
    data = {
            **request.form,
            'id':request.form['id']
        }
    Band.update(data)
    return redirect('/dashboard')