from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore
import datetime

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# CRIAR A TABELA ALL EVENTS 
@app.route('/create_all_events_table', methods=['POST'])
def create_all_events(): 
     all_events_data = {
        "currentEvent": None,
        "previousEvent": [],
        "wallet": {"id": None, "value": None},
        "users": []
    }
     
     db.collection('AllEvents').document('all_events').set(all_events_data)
     return jsonify({"message": "Collection succesfull created"})

# CRIAR UM EVENTO EM CURRENT EVENT 
@app.route('/create_event', methods=['POST'])
def create_event():
     try:
            # Obtenha os dados do evento a partir do corpo da solicitação
            # event_data = request.json
            event_data = {
                "id": "currentEvent",
                "eventName": "Primeiro Integration",
                "eventDate": "15/02/2024",
                "eventMembers": [],
                "quiz": [],
                "finance": None,
                "activeEvent": True,
                "task": None,
                "financeValidation": {"title": "Você irá participar financeiramente do evento?", "collaborators": []}
            }

            # Certifique-se de que os dados do evento não estão vazios
            if not event_data:
                return jsonify({"error": "Dados do evento ausentes"}), 400

            # Gere um ID único para o evento
            # evento_id = "currentEvent"
            event_id = event_data.get('id')

            # Adicione o evento à coleção 'AllEvents'
            db.collection('CurrentEvent').document(event_id).set(event_data)

            # Obtenha a referência do documento AllEvents
            all_events_ref = db.collection('AllEvents').document('all_events')

            # Atualize o campo currentEvent com a referência ao novo evento
            all_events_ref.update({"currentEvent": db.document(f'Eventos/{event_id}')})

            return jsonify({"message": f"Evento {event_id} adicionado à coleção AllEvents com sucesso!"})
     except Exception as error:
            print(f"Error occurred while searching for events: {error}")
            return jsonify({"error": f"Erro ao adicionar evento: {str(error)}"}), 500
      

# CRIAR ENQUETE 
@app.route('/create_quiz', methods=['POST'])
def create_quiz():
      try: 
            # Obtenha os dados do evento a partir do corpo da solicitação
            # quiz_data = request.json

            quiz_data = {
                  "id": "quiz1",
                  "title": "Votação esporte",
                  "category": "ACTIVITIES",
                  "answerType": "UNIQUE",
                  "answerOptions": [
                        {
                              "id": "answerXPTO1",
                              "title": "Sei la",
                              "votes": 0
                        },
                        {
                              "id": "answerXPTO2",
                              "title": "Nao sei",
                              "votes": 0
                        },
                  ]
            }

            if not quiz_data: 
                  return jsonify({"error": "Dados do quiz ausentes"}), 400
            
            quiz_id = quiz_data.get('id')

            # Adicione o Quiz a 'Quizzes' na coleção 'currentEvent' em 'AllEvents'
            current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference

            if current_event_ref:
                db.collection('Quizzes').document(quiz_id).set(quiz_data)
                current_event_ref.update({"quiz": firestore.ArrayUnion([db.document(f'Quizzes/{quiz_id}')])})

                return jsonify({"message": f"Quiz {quiz_id} adicionado a currentEvent com sucesso!"})
            else:
                return jsonify({"error": "currentEvent não encontrado"}), 404

      except Exception as error:
            print(f"Erro ao criar novo Quiz: {error}")
            return jsonify({"error": f"Erro ao criar novo Quiz: {str(error)}"}), 500