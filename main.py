from flask import Flask, jsonify
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Função para converter um documento Firestore para um dicionário serializável
def firestore_to_dict(doc):
    data = doc.to_dict()

    # Converta as referências do documento em dicionários antes de retornar
    for key, value in data.items():
        if isinstance(value, firestore.DocumentReference):
            data[key] = firestore_to_dict(value.get())

    data['id'] = doc.id
    return data

# Rota para obter todas as informações do documento all_events dentro da coleção AllEvents
@app.route('/get_all_events', methods=['GET'])
def get_all_events():
    try:
        # Obtenha a referência do documento all_events dentro da coleção AllEvents
        all_events_doc_ref = db.collection('AllEvents').document('all_events')

        # Obtenha os dados do documento all_events
        all_events_data = firestore_to_dict(all_events_doc_ref.get())

        return jsonify(all_events_data)

    except Exception as error:
        print(f"Error occurred while retrieving AllEvents: {error}")
        return jsonify({"error": f"Erro ao obter AllEvents: {str(error)}"}), 500

if __name__ == '__main__':
   app.run(debug=True)
