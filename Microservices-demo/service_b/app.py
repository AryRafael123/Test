from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/call-a')
def call_a():
    try:
        res = requests.get("http://service_a:5000/ping", timeout=3)
        return jsonify(from_a=res.json())
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
