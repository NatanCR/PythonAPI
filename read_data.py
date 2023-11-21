# from flask import Flask, jsonify
# from google.cloud import firestore
# from google.oauth2.service_account import Credentials
# import os
# app = Flask(__name__)

# # carregando as credenciais do JSON
# credentials = Credentials.from_service_account_file(os.environ.get
#                                                     ('GOOGLE_APPLICATION_CREDENTIALS'))
# db = firestore.Client(credentials=credentials)
# # inicializando o firestore com a credencial

# # Rota para obter dados de usuários
# @app.route('/get_users', methods=['GET'])
# def get_users():
#     try:
#         users = []

#         # Obtém todos os documentos da coleção 'usuarios'
#         users_ref = db.collection('usuarios').stream()

#         for user in users_ref:
#             users_data = user.to_dict()
#             users.append(users_data)

#         return jsonify({'usuarios': users})
#     except Exception as error:
#         print(f"Error occured while searching for users: {error}")
#         return jsonify({'error': 'Error occurred while searching for users'})

# #obter dados de eventos
# @app.route('/get_events', methods=['GET'])
# def get_events():
#   try: 
#       events = []
#       events_ref = db.collection('eventos').stream()

#       for event in events_ref:
#           event_data = event.to_dict()
#           events.append(event_data)
#       return jsonify({'eventos': events})
#   except Exception as error: 
#       print(f"Error occurred while searching for events: {error}")
#       return jsonify({'error': 'Error occurred while searching for events'})

# if __name__ == '__main__':
#    app.run(debug=True)

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

# TRATAR OS DADOS DO BANCO COM ISINSTANCE 
def serialize_data(data):
    if isinstance(data, firestore.DocumentReference):
        return serialize_data(data.get().to_dict())
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    else:
        return data

# PEGAR EVENTO ATUAL 
@app.route('/get_current_event', methods=['GET'])
def get_current_event():
    try: 
        currentEvent = []

        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get()
        
        if current_event_ref.exists:
            current_event_data = current_event_ref.to_dict()

            current_event_data_serialized = serialize_data(current_event_data)

            currentEvent.append(current_event_data_serialized)

        return jsonify({'CurrentEvent': currentEvent}), 200
        
    except Exception as error:
        print(f"Error occurred while retrieving CurrentEvent: {error}")
        return jsonify({"error": f"Erro ao obter CurrentEvent: {str(error)}"}), 500

# PEGAR TABELA DE ALL EVENTS
@app.route('/get_all_events', methods=['GET'])
def get_all_events():
    try: 
        allEvents = []

        all_events_ref = db.collection('AllEvents').document('all_events').get()
        
        if all_events_ref.exists:
            all_events_data = all_events_ref.to_dict()

            current_event_data_serialized = serialize_data(all_events_data)

            allEvents.append(current_event_data_serialized)

        return jsonify({'AllEvents': allEvents}), 200
        
    except Exception as error:
        print(f"Error occurred while retrieving AllEvents: {error}")
        return jsonify({"error": f"Erro ao obter AllEvents: {str(error)}"}), 500

if __name__ == '__main__':
   app.run(debug=True)
