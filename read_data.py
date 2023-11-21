# from flask import Flask, jsonify
# from google.cloud import firestore
# from google.oauth2.service_account import Credentials
# import os
# app = Flask(__name__)

# # carregando as credenciais do JSON
# credentials = Credentials.from_service_account_file(os.environ.get
#                                                     ('GOOGLE_APPLICATION_CREDENTIALS'))
# db = firestore.Client(credentials=credentials)
# # inicializando o firestore com a credencial

# # Rota para obter dados de usuários
# @app.route('/get_users', methods=['GET'])
# def get_users():
#     try:
#         users = []

#         # Obtém todos os documentos da coleção 'usuarios'
#         users_ref = db.collection('usuarios').stream()

#         for user in users_ref:
#             users_data = user.to_dict()
#             users.append(users_data)

#         return jsonify({'usuarios': users})
#     except Exception as error:
#         print(f"Error occured while searching for users: {error}")
#         return jsonify({'error': 'Error occurred while searching for users'})

# #obter dados de eventos
# @app.route('/get_events', methods=['GET'])
# def get_events():
#   try: 
#       events = []
#       events_ref = db.collection('eventos').stream()

#       for event in events_ref:
#           event_data = event.to_dict()
#           events.append(event_data)
#       return jsonify({'eventos': events})
#   except Exception as error: 
#       print(f"Error occurred while searching for events: {error}")
#       return jsonify({'error': 'Error occurred while searching for events'})

# if __name__ == '__main__':
#    app.run(debug=True)