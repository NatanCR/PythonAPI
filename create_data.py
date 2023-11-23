from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore

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
                "task": [],
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
            all_events_ref.update({"currentEvent": db.document(f'CurrentEvent/{event_id}')})

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
                  "id": "quiz1", #gerar aleatorio 
                  "title": "Votação esporte",
                  "category": "ACTIVITIES",
                  "answerType": "UNIQUE",
                  "answerOptions": [
                        {
                              "id": "answerXPTO1", #usar o title como id 
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
      
# CRIAR TASK 
@app.route('/create_event_task', methods=['POST'])
def create_event_task():
    try:
        # Obtenha os dados da tarefa a partir do corpo da solicitação
        # task_data = request.json

        task_data = {
            "id": "task1",  # Gerar aleatório
            "title": "Reunião",
            "deadline": "2023-12-01",
            "collaborators": [
            #     {
            #         "id": "member1",  # Substitua pelo ID real do colaborador
            #         "name": "João",
            #         "financeMember": True
            #     }
            ],
            "status": "ON",
            "icon": "meeting"
        }

        if not task_data:
            return jsonify({"error": "Dados da tarefa ausentes"}), 400

        task_id = task_data.get('id')

        # Adicione a tarefa a 'EventTasks' na coleção 'currentEvent' em 'AllEvents'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference

        if current_event_ref:
            db.collection('EventTasks').document(task_id).set(task_data)
            current_event_ref.update({"task": firestore.ArrayUnion([db.document(f'EventTasks/{task_id}')])})

            return jsonify({"message": f"Tarefa {task_id} adicionada a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "currentEvent não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao criar nova tarefa: {error}")
        return jsonify({"error": f"Erro ao criar nova tarefa: {str(error)}"}), 500

# CRIAR FINANCEIRO
@app.route('/create_finance', methods=['POST'])
def create_finance():
    try:
        # Obtenha os dados da tabela financeira a partir do corpo da solicitação
        # finance_data = request.json

        finance_data = {
            "id": "finance1",  # Gerar aleatório
            "title": "Orçamento Geral",
            "deadline": "2023-12-31",
            "totalValue": 10000.0,
            "valueMembers": None
        }

        if not finance_data:
            return jsonify({"error": "Dados da tabela financeira ausentes"}), 400

        finance_id = finance_data.get('id')

        # Adicione a tabela financeira a 'Finances' na coleção 'currentEvent' em 'AllEvents'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference

        if current_event_ref:
            db.collection('Finances').document(finance_id).set(finance_data)
            current_event_ref.update({"finance": firestore.ArrayUnion([db.document(f'Finances/{finance_id}')])})

            return jsonify({"message": f"Tabela financeira {finance_id} adicionada a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "currentEvent não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao criar nova tabela financeira: {error}")
        return jsonify({"error": f"Erro ao criar nova tabela financeira: {str(error)}"}), 500
    
    # CRIAR TABELA USER LOGIN 
@app.route('/create_user_table', methods=['POST'])
def create_user_table():
    try:
        # Certifique-se de que a coleção não existe antes de adicionar um documento
        users_collection_ref = db.collection('Users')
        if users_collection_ref.get():
            return jsonify({"error": "A coleção de usuários já existe"}), 400

        # Adicione um documento vazio à coleção para criar a coleção
        users_collection_ref.add({})

        return jsonify({"message": "Coleção de usuários criada com sucesso!"})

    except Exception as error: 
         print(f"Error ocurred while searching for events: {error}")
         return jsonify({"error": f"Erro ao criar user: {str(error)}"}), 500
    

# CRIAR USER 
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        user_data = {
             "id": "User1",
             "name": "User1",
             "email": "user1@gmail.com",
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
