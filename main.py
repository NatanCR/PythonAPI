from flask import Flask, jsonify
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# CRIAR USER 
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        user_data = {
             "id": "User2",
             "name": "User2",
             "email": "user2@gmail.com",
             "password": "12345"
        }

        if not user_data:
             return jsonify({"error": "Dados do usuário ausentes"}), 400

        user_id = user_data.get('id')

        users_collection_ref = db.collection('Users')

        if users_collection_ref:
            db.collection('Users').document(user_id).set(user_data)

            return jsonify({"message": f"User {user_id} criado com sucesso!"})
        else:
            return jsonify({"error": f"Erro ao criar novo user: {str(error)}"}), 500
    
    except Exception as error: 
         print(f"Error ocurred while searching for events: {error}")
         return jsonify({"error": f"Erro ao criar user: {str(error)}"}), 500


if __name__ == '__main__':
   app.run(debug=True)
