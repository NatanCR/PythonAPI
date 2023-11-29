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
        all_events_ref = db.collection('AllEvents').document('all_events')
        all_events_doc = all_events_ref.get()

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
