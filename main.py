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

# ADICIONAR MEMBRO NO EVENTO 
@app.route('/add_event_member', methods=['POST'])
def add_event_member():
    try:
        # Obtenha os dados do membro a partir do corpo da solicitação
        member_data = {
            "id": "Natan",  
            "name": "Natan",
            "financeMember": True
        }

        if not member_data:
            return jsonify({"error": "Dados do membro ausentes"}), 400

        member_id = member_data.get('id')

        # Adicione o membro a 'Members' na coleção 'currentEvent' em 'AllEvents'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference

        if current_event_ref:
            db.collection('Members').document(member_id).set(member_data)
            current_event_ref.update({"eventMembers": firestore.ArrayUnion([db.document(f'Members/{member_id}')])})

            return jsonify({"message": f"Membro {member_id} adicionado a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "currentEvent não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao adicionar novo membro: {error}")
        return jsonify({"error": f"Erro ao adicionar novo membro: {str(error)}"}), 500


if __name__ == '__main__':
   app.run(debug=True)
