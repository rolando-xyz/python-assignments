from flask import Flask, session

app = Flask(__name__)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = "rootroot"