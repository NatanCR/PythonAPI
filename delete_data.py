from flask import Flask, jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("service_firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

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

    
if __name__ == '__main__':
   app.run(debug=True)