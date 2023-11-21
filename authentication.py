from flask import Flask, jsonify, request
from firebase_admin import credentials, initialize_app, auth
import pyrebase
import json
import firebase_admin

app = Flask(__name__)

cred = credentials.Certificate("service_firebase.json") 
firebase_admin.initialize_app(cred)


#como registrar uma pessoa ex: /register?email=barbara@gmail.com&password=123456

config = {
    'apiKey': "AIzaSyDQ_i5-_zD9meDLhuyeqiJ_6Xojc1GPo_c",
    'authDomain': "integration-e8481.firebaseapp.com",
    'projectId': "integration-e8481",
    'storageBucket': "integration-e8481.appspot.com",
    'messagingSenderId': "930857685410",
    'appId': "1:930857685410:web:cb6d51cf5530886f48e2fb",
    'measurementId': "G-F4W9960VND",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/registerUser', methods=['GET', 'POST'])
def register():
    email = request.args.get('email')
    password = request.args.get('password')

    if not email or not password:
        return jsonify({'error': 'Parâmetros incompletos'}), 400

    if not email.endswith('@gmail.com'):
        return jsonify({'error': 'Apenas e-mails com o domínio @gmail.com podem se cadastrar'}), 400

    try:
        # criando o usuario
        user = auth.create_user_with_email_and_password(email, password)

        # acessando o 'idToken' do usuario para possíveis consultas
        id_token = user['idToken']

        # informações da conta
        info = auth.get_account_info(id_token)
        # o ID da pessoa sai como 'localId'
        print(info)

        # converte um objeto em uma string JSON
        user_json = json.dumps(user)

        # o ID da pessoa sai como 'localId'
        print(user_json)

        # mandando por e-mail (FUNCIONANDO)
        auth.send_email_verification(user['idToken'])

        auth.send_password_reset_email(email)

        return jsonify({'success': True, 'message': 'Usuário cadastrado com sucesso'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_authenticateUsers', methods=['GET'])
def get_usuarios():
    auth = firebase.auth()
    users = []

    # Example: Fetch user by UID
    uid = 'your_user_uid'
    user_by_uid = auth.get_account_info(uid)
    users.append({
        "uid": user_by_uid['users'][0]['localId'],
        "email": user_by_uid['users'][0]['email'],
        # Add other user properties as needed
    })

    # Example: Fetch user by email
    email = 'user@example.com'
    try:
        user_by_email = auth.get_account_info(email)
        users.append({
            "uid": user_by_email['users'][0]['localId'],
            "email": user_by_email['users'][0]['email'],
            # Add other user properties as needed
        })
    except:
        print(f"User with email {email} not found.")

    # Save users list to JSON file
    with open("output.json", "w") as outfile:
        json.dump(users, outfile)

    # Optionally, you can return the users as a JSON response
    return jsonify(users)

if __name__ == '__main__':
   app.run(debug=True)