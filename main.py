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


# Rota para obter dados de usuários
@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        users = []

        # Obtém todos os documentos da coleção 'usuarios'
        users_ref = db.collection('usuarios').stream()
        for user in users_ref:
            # Converte o documento para um dicionário
            user_data = user.to_dict()
            # Verifica se há campos que são referências a outros documentos
            for key, value in user_data.items():
                if isinstance(value, firestore.DocumentReference):
                    # Se for uma referência, substitua pelo ID do documento referenciado
                    user_data[key] = value.id
            users.append(user_data)
        return jsonify({'usuarios': users}), 200
    except Exception as error:
        print(f"Error occured while searching for users: {error}")
        return jsonify({'error': 'Error occurred while searching for users'}), 500

#obter dados de eventos
@app.route('/get_events', methods=['GET'])
def get_events():
  try: 
      events = []

      events_ref = db.collection('eventos').stream()
      for event in events_ref:
          event_data = event.to_dict()

          for key,value in event_data.items():
            if isinstance(value, firestore.DocumentReference):
                event_data[key] = value.id

          events.append(event_data)
      return jsonify({'eventos': events}), 200
  except Exception as error: 
      print(f"Error occurred while searching for events: {error}")
      return jsonify({'error': 'Error occurred while searching for events'}), 500

if __name__ == '__main__':
   app.run(debug=True)
