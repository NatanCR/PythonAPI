from flask import Flask, jsonify

from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

if __name__ == '__main__':
   app.run(debug=True)




