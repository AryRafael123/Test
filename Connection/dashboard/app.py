from flask import Flask, jsonify
import requests

app = Flask(__name__)

AUTH_SERVICE_URL = "http://auth:5000"

@app.route('/')
def home():
    return jsonify({"message": "Dashboard microservice running!"})

@app.route('/auth-status')
def auth_status():
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/")
        return jsonify({
            "dashboard": "connected",
            "auth_service_response": response.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
