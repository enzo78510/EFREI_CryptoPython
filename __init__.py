from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm31

key = Fernet.generate_key()
f = Fernet(key)
                                                                                                                                             
@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.get_json()
        key = data['key']
        value = data['value']

        # Vérifie que la clé est valide
        f = Fernet(key)
        value_bytes = value.encode()  # Conversion str -> bytes
        token = f.encrypt(value_bytes)  # Chiffrement
        return jsonify({"encrypted_value": token.decode()})
    except Exception as e:
        return jsonify({"error": f"Erreur lors du chiffrement : {str(e)}"}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():

    try:
        data = request.get_json()
        key = data['key']
        encrypted_value = data['value']

        # Vérifie que la clé est valide
        f = Fernet(key)
        encrypted_bytes = encrypted_value.encode()  # Conversion str -> bytes
        decrypted_value = f.decrypt(encrypted_bytes)  # Décryptage
        return jsonify({"decrypted_value": decrypted_value.decode()})
    except Exception as e:
        return jsonify({"error": f"Erreur lors du décryptage : {str(e)}"}), 400

@app.route('/generate-key', methods=['GET'])
def generate_key():
    """
    Génère une clé unique pour l'utilisateur.
    """
    key = Fernet.generate_key()
    return jsonify({"key": key.decode()})

if __name__ == "__main__":
    app.run(debug=True)
