from flask import Flask, jsonify, request
import pyrebase
import json

app = Flask(__name__)

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

@app.route('/register', methods=['GET'])
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


if __name__ == '__main__':
   app.run(debug=True)