from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify(message="pong from service A")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
