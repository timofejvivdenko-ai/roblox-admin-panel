from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Це дозволить твоєму сайту на GitHub спілкуватися з цим сервером

storage = {"cmd": "Очікування..."}

@app.route('/get')
def get_cmd():
    return jsonify({"command": storage["cmd"]})

@app.route('/set')
def set_cmd():
    storage["cmd"] = request.args.get('text', 'No command')
    return "Команду змінено!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
