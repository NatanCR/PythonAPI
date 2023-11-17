import pyrebase
import json

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

email = 'barbara.argolo@gmail.com'
password = '123456'

if not email.endswith('@gmail.com'):
    print('Apenas e-mails com o domínio @gmail.com podem se cadastrar')
else:
    user = auth.create_user_with_email_and_password(email, password)

# criando o usuario

# acessando o'idToken' do usuario para possiveis consultas
id_token = user['idToken']

#informaçoes da conta
info = auth.get_account_info(id_token)
#o ID da pessoa sai como 'localId'
print(info)

# converte um objeto em uma string JSON
user_json = json.dumps(user)

#o ID da pessoa sai como 'localId'
print(user_json)

#mandando por e-mail (FUNCIONANDO)
auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)
