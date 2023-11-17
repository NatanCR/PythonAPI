from flask import Flask, jsonify
from google.cloud import firestore
# from google.oauth2.service_account import Credentials
# import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# carregando as credenciais do JSON
# credentials = Credentials.from_service_account_file(os.environ.get
#                                                     ('GOOGLE_APPLICATION_CREDENTIALS'))
# db = firestore.Client(credentials=credentials)
# inicializando o firestore com a credencial



if __name__ == '__main__':
   app.run(debug=True)
