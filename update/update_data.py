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