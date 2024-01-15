from flask import Blueprint, redirect, render_template
from firebase_admin import db
import os

cred_obj = firebase_admin.credentials.Certificate('../keyService.json')
default_app = firebase_admin.initialize_app(cred_obj,  {
	'databaseURL': 'https://url-shrinker-client-default-rtdb.firebaseio.com/'
	})
app = Blueprint('main', __name__)

@app.route("/")
def hello_world():
    return redirect("/app")

@app.route("/app")
def homepage():
    return render_template('index.html')

@app.route('/<path:generatedKey>', methods=['GET'])
def fetch_from_firebase(generatedKey):
    ref = db.reference("/"+ generatedKey)
    data = ref.get()
    if not data:
        return '404 not found'
    else:
        longURL = data['longURL']
        return redirect(longURL)