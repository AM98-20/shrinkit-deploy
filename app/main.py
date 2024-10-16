from flask import Flask, redirect, render_template
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

# Construct the service account info
service_account_info = {
  "type": "service_account",
  "project_id": os.environ.get("PROJECT_ID"),
  "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
  "private_key": os.environ.get("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.environ.get("CLIENT_EMAIL"),
  "client_id": os.environ.get("CLIENT_ID"),
  "auth_uri": os.environ.get("AUTH_URI"),
  "token_uri": os.environ.get("TOKEN_URI"),
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-t9z5d%40url-shrinker-client.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Initialize the Firebase Admin SDK
cred = credentials.Certificate(service_account_info)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://url-shrinker-client-default-rtdb.firebaseio.com/'
})

# Initialize Flask app
app = Flask(__name__, static_folder='./build/static', template_folder="./build")

@app.route("/")
def hello_world():
    return redirect("/app")

@app.route("/app")
def homepage():
    return render_template('index.html')

@app.route('/<path:generatedKey>', methods=['GET'])
def fetch_from_firebase(generatedKey):
    # Ignore requests for favicon.ico and manifest.json
    if generatedKey in ["favicon.ico", "manifest.json"]:
        return '404 Not Found', 404

    ref = db.reference("/" + generatedKey)
    data = ref.get()

    if not data:
        return '404 Not Found', 404
    else:
        longURL = data.get('longURL')
        if longURL:
            return redirect(longURL)
        else:
            return 'Invalid data format', 400

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)