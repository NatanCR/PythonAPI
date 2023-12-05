from flask import Flask, Blueprint, jsonify, request
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# /////////////////////
# READ DATA 
# /////////////////////

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
        # Modificar a referência para apontar para a coleção AllEvents e o documento AllEvents
        all_events_ref = db.collection('AllEvents').document('AllEvents').get()
        
        if all_events_ref.exists:
            all_events_data = all_events_ref.to_dict()

            # Acessar o campo currentEvent diretamente
            current_event_data = all_events_data.get('currentEvent')

            if current_event_data:
                current_event_data_serialized = serialize_data(current_event_data)
                return jsonify({'CurrentEvent': current_event_data_serialized}), 200

        return jsonify({"error": "Nenhum evento atual encontrado"}), 404
        
    except Exception as error:
        print(f"Error occurred while retrieving CurrentEvent: {error}")
        return jsonify({"error": f"Erro ao obter CurrentEvent: {str(error)}"}), 500

# PEGAR TABELA DE ALL EVENTS
@app.route('/get_all_events', methods=['GET'])
def get_all_events():
    try: 
        allEvents = []

        all_events_ref = db.collection('AllEvents').document('AllEvents').get()
        
        if all_events_ref.exists:
            all_events_data = all_events_ref.to_dict()

            current_event_data_serialized = serialize_data(all_events_data)

            allEvents.append(current_event_data_serialized)

        return jsonify({'AllEvents': allEvents}), 200
        
    except Exception as error:
        print(f"Error occurred while retrieving AllEvents: {error}")
        return jsonify({"error": f"Erro ao obter AllEvents: {str(error)}"}), 500
    


# /////////////////////
# CREATE DATA 
# /////////////////////


# CRIAR USER 
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # user_data = {
        #      "id": "User1",
        #      "name": "User1",
        #      "email": "user1@gmail.com",
        #      "password": "12345"
        # }
        user_data = request.json

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

# CRIAR A TABELA ALL EVENTS 
@app.route('/create_all_events_table', methods=['POST'])
def create_all_events(): 
    try:
        all_events_data = request.json
        # all_events_data = {
        #     "currentEvent": None,
        #     "previousEvent": [],
        #     "wallet": {"id": None, "value": None},
        #     "users": []
        # }
        if not all_events_data:
            return jsonify({"error": "Dados de allEvents ausentes"})
        all_events_data_id = all_events_data.get('id')
            
        db.collection('AllEvents').document(all_events_data_id).set(all_events_data)
        return jsonify({"message": "Collection succesfull created"})
    except Exception as error:
            print(f"Error occurred while searching for events: {error}")
            return jsonify({"error": f"Erro ao criar tabela: {str(error)}"}), 500

# # CRIAR UM EVENTO EM CURRENT EVENT 
# @app.route('/create_event', methods=['POST'])
# def create_event():
#      try:
#             # Obtenha os dados do evento a partir do corpo da solicitação
#             # event_data = request.json
#             event_data = {
#                 "id": "currentEvent",
#                 "eventName": "Primeiro Integration",
#                 "eventDate": "15/02/2024",
#                 "eventMembers": [],
#                 "quiz": [],
#                 "finance": None,
#                 "activeEvent": True,
#                 "task": [],
#                 "financeValidation": {"title": "Você irá participar financeiramente do evento?", "collaborators": []}
#             } 

#             # Certifique-se de que os dados do evento não estão vazios
#             if not event_data:
#                 return jsonify({"error": "Dados do evento ausentes"}), 400

#             # Gere um ID único para o evento
#             # evento_id = "currentEvent"
#             event_id = event_data.get('id')

#             # Adicione o evento à coleção 'AllEvents'
#             db.collection('CurrentEvent').document(event_id).set(event_data)

#             # Obtenha a referência do documento AllEvents
#             all_events_ref = db.collection('AllEvents').document('all_events')

#             # Atualize o campo currentEvent com a referência ao novo evento
#             all_events_ref.update({"currentEvent": db.document(f'CurrentEvent/{event_id}')})

#             return jsonify({"message": f"Evento {event_id} adicionado à coleção AllEvents com sucesso!"})
#      except Exception as error:
#             print(f"Error occurred while searching for events: {error}")
#             return jsonify({"error": f"Erro ao adicionar evento: {str(error)}"}), 500
      

# CRIAR ENQUETE 
@app.route('/create_quiz', methods=['POST'])
def create_quiz():
    try:
        # Obtenha os dados do quiz a partir do corpo da solicitação
        quiz_data = request.json

        # quiz_data = {
        #     "id": "quiz1", #gerar aleatorio 
        #     "title": "Votação esporte",
        #     "category": "ACTIVITIES",
        #     "answerType": "UNIQUE",
        #     "answerOptions": [
        #         {
        #             "id": "answerXPTO1", #usar o title como id 
        #             "title": "Sei la",
        #             "votes": 0
        #         },
        #         {
        #             "id": "answerXPTO2",
        #             "title": "Nao sei",
        #             "votes": 0
        #         },
        #     ]
        # }

        if not quiz_data:
            return jsonify({"error": "Dados do quiz ausentes"}), 400

        quiz_id = quiz_data.get('id')

        # Modifique a referência para apontar para a coleção 'AllEvents' e o documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents').get().reference

        if all_events_ref:
            # Atualize o campo 'quizzes' dentro de 'currentEvent' em 'AllEvents'
            all_events_ref.update({"currentEvent.quiz": firestore.ArrayUnion([quiz_data])})

            return jsonify({"message": f"Quiz {quiz_id} adicionado a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "AllEvents não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao criar novo Quiz: {error}")
        return jsonify({"error": f"Erro ao criar novo Quiz: {str(error)}"}), 500
      
# CRIAR TASK 
@app.route('/create_task', methods=['POST'])
def create_event_task():
    try:
        # Obtenha os dados da tarefa a partir do corpo da solicitação
        task_data = request.json

        # task_data = {
        #     "id": "task1",  # Gerar aleatório
        #     "title": "Reunião",
        #     "deadline": "2023-12-01",
        #     "collaborators": [
        #         {
        #             "id": "member1",  # Substitua pelo ID real do colaborador
        #             "name": "João",
        #             "financeMember": True
        #         }
        #     ],
        #     "status": "ON",
        #     "icon": "meeting"
        # }

        if not task_data:
            return jsonify({"error": "Dados da tarefa ausentes"}), 400

        task_id = task_data.get('id')

        # Modifique a referência para apontar para a coleção 'AllEvents' e o documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents').get().reference

        if all_events_ref:
            # Atualize o campo 'tasks' dentro de 'currentEvent' em 'AllEvents'
            all_events_ref.update({"currentEvent.task": firestore.ArrayUnion([task_data])})

            return jsonify({"message": f"Tarefa {task_id} adicionada a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "AllEvents não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao criar nova tarefa: {error}")
        return jsonify({"error": f"Erro ao criar nova tarefa: {str(error)}"}), 500

# CRIAR FINANCEIRO
@app.route('/create_finance', methods=['POST'])
def create_finance():
    try:
        # Obtenha os dados da tabela financeira a partir do corpo da solicitação
        finance_data = request.json

        # finance_data = {
        #     "id": "finance1",  # Gerar aleatório
        #     "title": "Orçamento Geral",
        #     "deadline": "2023-12-31",
        #     "totalValue": 10000.0,
        #     "valueMembers": None
        # }

        if not finance_data:
            return jsonify({"error": "Dados da tabela financeira ausentes"}), 400

        finance_id = finance_data.get('id')

        # Modifique a referência para apontar para a coleção 'AllEvents' e o documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents').get().reference

        if all_events_ref:
            # Atualize o campo 'finances' dentro de 'currentEvent' em 'AllEvents'
            all_events_ref.update({"currentEvent.finance": firestore.ArrayUnion([finance_data])})

            return jsonify({"message": f"Tabela financeira {finance_id} adicionada a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "AllEvents não encontrado"}), 404

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




# /////////////////////
# DELETE DATA 
# /////////////////////

    
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


# /////////////////////
# UPDATE DATA 
# /////////////////////
    
# ADICIONAR VALOR NA CARTEIRA
@app.route('/add_wallet_value', methods=['POST'])
def add_wallet_value():
      try: 
           # Obtenha os dados do evento a partir do corpo da solicitação
            wallet_data = request.json 

            # wallet_data = {
            #       "id": "wallet",
            #       "value": 0.00
            # }

            walle_value = wallet_data.get('value')

            if not wallet_data: 
                  return jsonify({"error": "Dados da carteira ausentes"}), 400
            
            all_events_ref = db.collection('AllEvents').document('AllEvents')
            # ATUALIZA A WALLET INTEIRA 
            # all_events_ref.update({"wallet": wallet_data})
            
            # ATUALIZA O VALUE DA WALLET 
            all_events_ref.update({"wallet.value": walle_value})

            return jsonify({"message": "Wallet atualizada com sucesso"})
      
      except Exception as error:
            print(f"Erro ao atualizar wallet: {error}")
            return jsonify({"error": f"Erro ao atualizar wallet: {str(error)}"}), 500
      
# ADICIONAR MEMBRO NO EVENTO 
@app.route('/add_event_member', methods=['POST'])
def add_event_member():
    try:
        # Obtenha os dados do membro a partir do corpo da solicitação
        member_data = request.json
        
        # member_data = {
        #     "id": "Natan",  
        #     "name": "Natan",
        #     "financeMember": True
        # }

        if not member_data:
            return jsonify({"error": "Dados do membro ausentes"}), 400

        member_id = member_data.get('id')

        # Modifique a referência para apontar para a coleção 'AllEvents' e o documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents').get().reference

        if all_events_ref:
            # Atualize o campo 'eventMembers' dentro de 'currentEvent' em 'AllEvents'
            all_events_ref.update({"currentEvent.eventMembers": firestore.ArrayUnion([member_data])})

            return jsonify({"message": f"Membro {member_id} adicionado a currentEvent com sucesso!"})
        else:
            return jsonify({"error": "AllEvents não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao adicionar novo membro: {error}")
        return jsonify({"error": f"Erro ao adicionar novo membro: {str(error)}"}), 500
    
# ADICIONAR MEMBRO EXISTENTE NA TASK 
@app.route('/add_member_to_task', methods=['POST'])
def add_collaborator_to_task():
    try:
        # Obtenha os dados da solicitação
        request_data = request.json

        # Verifique se o ID da task e o novo colaborador estão presentes nos dados da solicitação
        if not request_data or 'id' not in request_data or 'member' not in request_data:
            return jsonify({"error": "Dados inválidos na solicitação"}), 400

        # Obtenha o ID da task e o novo colaborador da solicitação
        task_id = request_data['id']
        new_collaborator = request_data['member']

        # Obtenha a referência do documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents')

        # Obtenha os dados atuais do 'AllEvents'
        all_events_data = all_events_ref.get().to_dict()

        # Encontre a task correspondente pelo ID
        task_to_update = next((task for task in all_events_data['currentEvent']['task'] if task['id'] == task_id), None)

        if not task_to_update:
            return jsonify({"error": f"Tarefa com ID {task_id} não encontrada"}), 404

        # Adicione o novo colaborador ao array 'collaborators' dentro da task
        task_to_update['collaborators'].append(new_collaborator)

        # Atualize o documento 'AllEvents' com os dados atualizados
        all_events_ref.update({"currentEvent": all_events_data['currentEvent']})

        return jsonify({"message": "Novo colaborador adicionado com sucesso!"})

    except Exception as error:
        print(f"Erro ao adicionar novo colaborador à task: {error}")
        return jsonify({"error": f"Erro ao adicionar novo colaborador à task: {str(error)}"}), 500
    
# ADICIONAR MEMBRO NA VOTAÇAO DO FINANCEIRO
@app.route('/add_member_to_finance_validation', methods=['POST'])
def add_member_to_finance_validation():
    try:
        # Obtenha os dados da solicitação
        request_data = request.json

        # Verifique se o ID do evento e o novo membro estão presentes nos dados da solicitação
        if not request_data or 'id' not in request_data or 'member' not in request_data:
            return jsonify({"error": "Dados inválidos na solicitação"}), 400

        # Obtenha o ID do evento e o novo membro da solicitação
        event_id = request_data['id']
        new_member = request_data['member']

        # Obtenha a referência do documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents')

        # Obtenha os dados atuais do 'AllEvents'
        all_events_data = all_events_ref.get().to_dict()

        # Obtenha o evento correspondente pelo ID
        event_to_update = all_events_data['currentEvent']

        # Verifique se o evento possui a chave 'financeValidation'
        if 'financeValidation' not in event_to_update:
            return jsonify({"error": "financeValidation não encontrada no evento"}), 404

        # Certifique-se de que 'collaborators' está presente em 'financeValidation'
        if 'collaborators' not in event_to_update['financeValidation']:
            event_to_update['financeValidation']['collaborators'] = []

        # Adicione o novo membro ao array 'collaborators' dentro de 'financeValidation'
        event_to_update['financeValidation']['collaborators'].append(new_member)

        # Atualize o documento 'AllEvents' com os dados atualizados
        all_events_ref.update({"currentEvent": event_to_update})

        return jsonify({"message": "Novo membro adicionado à financeValidation com sucesso!"})

    except Exception as error:
        print(f"Erro ao adicionar novo membro à financeValidation: {error}")
        return jsonify({"error": f"Erro ao adicionar novo membro à financeValidation: {str(error)}"}), 500
    
# ADICIONAR UM VOTO NA RESPOSTA DA ENQUETE - testar
@app.route('/increment_vote', methods=['POST'])
def increment_vote():
    try:
        # Obtenha os dados da solicitação
        request_data = request.json

        # Verifique se o ID do quiz, o ID da opção e o novo número de votos estão presentes nos dados da solicitação
        if not request_data or 'id' not in request_data or 'optionId' not in request_data:
            return jsonify({"error": "Dados inválidos na solicitação"}), 400

        # Obtenha o ID do quiz, o ID da opção e o novo número de votos da solicitação
        quiz_id = request_data['id']
        option_id = request_data['optionId']

        # Obtenha a referência do documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents')

        # Obtenha os dados atuais do 'AllEvents'
        all_events_data = all_events_ref.get().to_dict()

        # Encontre o quiz correspondente pelo ID
        quiz_to_update = next((quiz for quiz in all_events_data['currentEvent']['quiz'] if quiz['id'] == quiz_id), None)

        if not quiz_to_update:
            return jsonify({"error": f"Quiz com ID {quiz_id} não encontrado"}), 404

        # Encontre a opção correspondente pelo ID dentro do quiz
        option_to_update = next((option for option in quiz_to_update['answerOptions'] if option['optionId'] == option_id), None)

        if not option_to_update:
            return jsonify({"error": f"Opção com ID {option_id} não encontrada no quiz {quiz_id}"}), 404

        # Incrementar o número de votos para a opção específica
        option_to_update['votes'] += 1

        # Atualize apenas o campo 'votes' da opção específica
        all_events_ref.update({
            "currentEvent.quiz": all_events_data['currentEvent']['quiz']
        })

        return jsonify({"message": "Voto incrementado com sucesso!"})

    except Exception as error:
        print(f"Erro ao incrementar voto: {error}")
        return jsonify({"error": f"Erro ao incrementar voto: {str(error)}"}), 500
    
# MOVER EVENTO ATUAL PARA EVENTOS PASSADOS E LIMPAR EVENTO ATUAL
@app.route('/move_to_previous_event', methods=['POST'])
def move_to_previous_event():
    try:
        # Obtenha o documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents')
        all_events_doc = all_events_ref.get().to_dict()

        if not all_events_doc.exists:
            return jsonify({"error": "Documento AllEvents não encontrado"}), 404

        # Obtenha o 'currentEvent' do documento 'AllEvents'
        current_event = all_events_doc.to_dict().get('currentEvent')

        if not current_event:
            return jsonify({"error": "currentEvent não encontrado em AllEvents"}), 404

        # Atualize 'previousEvent' adicionando 'currentEvent' ao array
        all_events_ref.update({"previousEvent": firestore.ArrayUnion([current_event])})

        # Limpe 'currentEvent' definindo-o como None
        all_events_ref.update({"currentEvent": None})

        return jsonify({"message": "currentEvent movido para previousEvent em AllEvents com sucesso!"})

    except Exception as error:
        print(f"Erro ao mover currentEvent para previousEvent: {error}")
        return jsonify({"error": f"Erro ao mover currentEvent para previousEvent: {str(error)}"}), 500

# ATUALIZAR EVENTO ATUAL POR COMPLETO
@app.route('/update_current_event', methods=['POST'])
def update_current_event():
    try:
        # Obtenha os dados do currentEvent a partir do corpo da solicitação
        current_event_data = request.json

        if not current_event_data:
            return jsonify({"error": "Dados do currentEvent ausentes"}), 400

        # Obtenha a referência do documento 'AllEvents'
        all_events_ref = db.collection('AllEvents').document('AllEvents')

        # Atualize o campo 'currentEvent' com os novos dados
        all_events_ref.update({"currentEvent": current_event_data})

        return jsonify({"message": "currentEvent atualizado com sucesso!"})

    except Exception as error:
        print(f"Erro ao atualizar currentEvent: {error}")
        return jsonify({"error": f"Erro ao atualizar currentEvent: {str(error)}"}), 500
    
if __name__ == '__main__':
   app.run(debug=True)
