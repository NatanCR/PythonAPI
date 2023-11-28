from flask import Flask, jsonify, request
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


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

        # Modificar a referência para apontar para a coleção AllEvents e o documento AllEvents
        all_events_ref = db.collection('AllEvents').document('AllEvents').get()
        
        if all_events_ref.exists:
            all_events_data = all_events_ref.to_dict()

            # Acessar o campo currentEvent diretamente
            current_event_data = all_events_data.get('currentEvent')

            if current_event_data:
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

        all_events_ref = db.collection('AllEvents').document('AllEvents').get()
        
        if all_events_ref.exists:
            all_events_data = all_events_ref.to_dict()

            current_event_data_serialized = serialize_data(all_events_data)

            allEvents.append(current_event_data_serialized)

        return jsonify({'AllEvents': allEvents}), 200
        
    except Exception as error:
        print(f"Error occurred while retrieving AllEvents: {error}")
        return jsonify({"error": f"Erro ao obter AllEvents: {str(error)}"}), 500


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



if __name__ == '__main__':
   app.run(debug=True)




