
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

def serialize_data(data):
    if isinstance(data, firestore.DocumentReference):
        return serialize_data(data.get().to_dict())
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    else:
        return data

# Rota para obter todas as informações do documento all_events dentro da coleção AllEvents
@app.route('/get_all_events', methods=['GET'])
def get_all_events():
    try: 
        currentEvent = []

        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get()
        
        if current_event_ref.exists:
            current_event_data = current_event_ref.to_dict()

            current_event_data_serialized = serialize_data(current_event_data)

            currentEvent.append(current_event_data_serialized)

        return jsonify({'CurrentEvent': currentEvent}), 200
        
    except Exception as error:
        print(f"Error occurred while retrieving AllEvents: {error}")
        return jsonify({"error": f"Erro ao obter AllEvents: {str(error)}"}), 500

if __name__ == '__main__':
   app.run(debug=True)
