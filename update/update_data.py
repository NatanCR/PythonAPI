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
            # wallet_data = request.json 

            wallet_data = {
                  "id": "wallet",
                  "value": 0.00
            }

            walle_value = wallet_data.get('value')

            if not wallet_data: 
                  return jsonify({"error": "Dados da carteira ausentes"}), 400
            
            all_events_ref = db.collection('AllEvents').document('all_events')
            # ATUALIZA A WALLET INTEIRA 
            # all_events_ref.update({"wallet": wallet_data})
            
            # ATUALIZA O VALUE DA WALLET 
            # all_events_ref.update({"wallet.value": walle_value})

            return jsonify({"message": "Wallet atualizada com sucesso"})
      
      except Exception as error:
            print(f"Erro ao atualizar wallet: {error}")
            return jsonify({"error": f"Erro ao atualizar wallet: {str(error)}"}), 500
      
# ADICIONAR MEMBRO NO EVENTO 
@app.route('/add_event_member', methods=['POST'])
def add_event_member():
    try:
        # Obtenha os dados do membro a partir do corpo da solicitação
        # member_data = request.json
        
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
    
# ADICIONAR MEMBRO EXISTENTE NA TASK 
@app.route('/add_member_to_task', methods=['POST'])
def add_member_to_task():
    try:
        # Obtenha o ID do membro a partir do corpo da solicitação
        # member_id = request.json.get('id')
        member_data = {
            "id": "Gui",  
            "name": "Gui",
            "financeMember": True
        }
        member_id = member_data.get('id')

        if not member_id:
            return jsonify({"error": "ID do membro ausente"}), 400

        # Suponha que você tenha o ID da tarefa da solicitação (substitua 'task1' pelo ID real da tarefa)
        # task_id = request.json.get('id', 'task1')
        task = {
            "id": "task1"
        }
        task_id = task.get('id')

        # Adicione o membro existente à lista de colaboradores na tarefa específica
        task_ref = db.collection('EventTasks').document(task_id).get().reference
        if task_ref:
            member_ref = db.collection('Members').document(member_id).get().reference
            if member_ref:
                task_ref.update({"collaborators": firestore.ArrayUnion([member_ref])})

                return jsonify({"message": f"Membro {member_id} adicionado à tarefa {task_id} com sucesso!"})
            else:
                return jsonify({"error": f"Membro {member_id} não encontrado"}), 404
        else:
            return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404

    except Exception as error:
        print(f"Erro ao adicionar membro existente à tarefa: {error}")
        return jsonify({"error": f"Erro ao adicionar membro existente à tarefa: {str(error)}"}), 500
    
# ADICIONAR UM VOTO NA RESPOSTA DA ENQUETE 
@app.route('/increment_votes', methods=['POST'])
def increment_votes():
    try:
        # Obtenha os IDs do quiz e da QuizAnswer a partir do corpo da solicitação
        quiz = {
            "id": "quiz"
        }

        answer = {
            "id": "answerXPTO1"
        }

        quiz_id = quiz.get('id')
        answer_id = answer.get('id')

        if not quiz_id or not answer_id:
            return jsonify({"error": "IDs ausentes"}), 400

        # Suponha que você tenha o ID do quiz da solicitação
        quiz_ref = db.collection('Quizzes').document(quiz_id).get().reference

        if quiz_ref:
            # Obtenha o documento do quiz
            quiz_doc = quiz_ref.get().to_dict()

            # Obtenha o array de opções de resposta
            answer_options = quiz_doc.get('answerOptions', [])

            # Encontre a opção de resposta correta pelo ID
            for option in answer_options:
                if option.get('id') == answer_id:
                    # Incrementar o número de votos
                    option['votes'] = option.get('votes', 0) + 1

                    # Atualize o documento do quiz com a opção de resposta atualizada
                    quiz_ref.update({"answerOptions": answer_options})

                    return jsonify({"message": f"Voto incrementado para a resposta {answer_id} no quiz {quiz_id} com sucesso!"})

            # Se o loop terminar sem encontrar a opção, retorne um erro
            return jsonify({"error": f"QuizAnswer {answer_id} não encontrada no quiz {quiz_id}"}), 404

        else:
            return jsonify({"error": f"Quiz {quiz_id} não encontrado"}), 404

    except Exception as error:
        print(f"Erro ao incrementar votos: {error}")
        return jsonify({"error": f"Erro ao incrementar votos: {str(error)}"}), 500