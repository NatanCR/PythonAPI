from flask import Flask, Blueprint, jsonify
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore
from read_data import read_data_bp, serialize_data

app = Flask(__name__)
app.register_blueprint(read_data_bp)

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
@read_data_bp.route('/get_current_event', methods=['GET'])
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
@read_data_bp.route('/get_all_events', methods=['GET'])
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
    
# DELETAR EVENTO
@app.route('/delete_event/<string:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        # Verifique se o evento existe
        event_ref = db.collection('CurrentEvent').document(event_id)
        event = event_ref.get()
        if not event.exists:
            return jsonify({"error": f"Evento {event_id} não encontrado"}), 404

        # Remova o evento da coleção 'CurrentEvent'
        event_ref.delete()

        # Remova a referência ao evento da coleção 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('all_events')
        all_events_data = all_events_ref.get().to_dict()

        if all_events_data and all_events_data.get('currentEvent') == event_id:
            all_events_ref.update({"currentEvent": None})

        return jsonify({"message": f"Evento {event_id} excluído com sucesso!"})

    except Exception as error:
        print(f"Erro ao excluir evento: {error}")
        return jsonify({"error": f"Erro ao excluir evento: {str(error)}"}), 500
    
# DELETAR ENQUETE
@app.route('/delete_quiz/<string:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    try:
        # Verifique se a enquete existe
        quiz_ref = db.collection('Quizzes').document(quiz_id)
        quiz = quiz_ref.get()
        if not quiz.exists:
            return jsonify({"error": f"Enquete {quiz_id} não encontrada"}), 404

        # Remova a enquete da coleção 'Quizzes'
        quiz_ref.delete()

        # Remova a referência à enquete da coleção 'currentEvent' em 'AllEvents'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference
        if current_event_ref:
            current_event_ref.update({"quiz": firestore.ArrayRemove([db.document(f'Quizzes/{quiz_id}')])})

        return jsonify({"message": f"Enquete {quiz_id} excluída com sucesso!"})

    except Exception as error:
        print(f"Erro ao excluir enquete: {error}")
        return jsonify({"error": f"Erro ao excluir enquete: {str(error)}"}), 500
    
# DELETAR MEMBRO
@app.route('/delete_member/<string:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        # Verifique se o membro existe
        member_ref = db.collection('Members').document(member_id)
        member = member_ref.get()
        if not member.exists:
            return jsonify({"error": f"Membro {member_id} não encontrado"}), 404

        # Remova o membro da coleção 'Members'
        member_ref.delete()

        # Remova a referência ao membro da coleção 'eventMembers' em 'CurrentEvent'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference
        if current_event_ref:
            current_event_ref.update({"eventMembers": firestore.ArrayRemove([db.document(f'Members/{member_id}')])})

        return jsonify({"message": f"Membro {member_id} excluído com sucesso!"})

    except Exception as error:
        print(f"Erro ao excluir membro: {error}")
        return jsonify({"error": f"Erro ao excluir membro: {str(error)}"}), 500
    
# DELETAR CARTEIRA
@app.route('/delete_finance/<string:finance_id>', methods=['DELETE'])
def delete_finance(finance_id):
    try:
        # Verifique se a finança existe
        finance_ref = db.collection('Finances').document(finance_id)
        finance = finance_ref.get()
        if not finance.exists:
            return jsonify({"error": f"Finança {finance_id} não encontrada"}), 404

        # Remova a finança da coleção 'Finances'
        finance_ref.delete()

        # Remova a referência à finança da coleção 'finance' em 'CurrentEvent'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference
        if current_event_ref:
            current_event_ref.update({"finance": firestore.ArrayRemove([db.document(f'Finances/{finance_id}')])})

        return jsonify({"message": f"Finança {finance_id} excluída com sucesso!"})

    except Exception as error:
        print(f"Erro ao excluir finança: {error}")
        return jsonify({"error": f"Erro ao excluir finança: {str(error)}"}), 500
    
# DELETAR TAREFA
@app.route('/delete_event_task/<string:event_task_id>', methods=['DELETE'])
def delete_event_task(event_task_id):
    try:
        # Verifique se a tarefa de evento existe
        event_task_ref = db.collection('EventTasks').document(event_task_id)
        event_task = event_task_ref.get()
        if not event_task.exists:
            return jsonify({"error": f"Tarefa de evento {event_task_id} não encontrada"}), 404

        # Remova a tarefa de evento da coleção 'EventTasks'
        event_task_ref.delete()

        # Remova a referência à tarefa de evento da coleção 'task' em 'CurrentEvent'
        current_event_ref = db.collection('CurrentEvent').document('currentEvent').get().reference
        if current_event_ref:
            current_event_ref.update({"task": firestore.ArrayRemove([db.document(f'EventTasks/{event_task_id}')])})

        return jsonify({"message": f"Tarefa de evento {event_task_id} excluída com sucesso!"})

    except Exception as error:
        print(f"Erro ao excluir tarefa de evento: {error}")
        return jsonify({"error": f"Erro ao excluir tarefa de evento: {str(error)}"}), 500

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
    



if __name__ == '__main__':
   app.run(debug=True)
