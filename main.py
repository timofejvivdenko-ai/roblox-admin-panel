from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Тут зберігається останнє повідомлення
storage = {"message": ""}

# ПАРОЛЬ: має бути такий самий, як у Roblox Script!
ACCESS_KEY = "МійСуперСекретнийПароль123"

# 1. Головна сторінка (Твій сайт)
@app.route('/')
def index():
    # Простий дизайн сайту прямо в коді
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Roblox Admin</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background: #222; color: white; }
                input { padding: 10px; width: 250px; border-radius: 5px; border: none; }
                button { padding: 10px 20px; background: #00A2FF; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background: #0082CC; }
            </style>
        </head>
        <body>
            <h1>Панель керування Roblox</h1>
            <input type="text" id="msg" placeholder="Введіть текст для консолі...">
            <button onclick="send()">Відправити</button>

            <script>
                async function send() {
                    const text = document.getElementById('msg').value;
                    const response = await fetch('/send', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: text, key: "''' + ACCESS_KEY + '''" })
                    });
                    if (response.ok) { alert("Відправлено в чергу!"); }
                    else { alert("Помилка доступу!"); }
                }
            </script>
        </body>
        </html>
    ''')

# 2. Шлях для отримання даних від сайту
@app.route('/send', methods=['POST'])
def send():
    data = request.json
    if data.get("key") == ACCESS_KEY:
        storage["message"] = data.get("message", "")
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "forbidden"}), 403

# 3. Шлях для видачі даних Роблоксу
@app.route('/get_for_roblox', methods=['GET'])
def get_for_roblox():
    # Перевіряємо ключ, який надсилає Roblox
    key = request.args.get("key")
    if key == ACCESS_KEY:
        msg = storage["message"]
        storage["message"] = "" # Очищуємо після видачі
        return jsonify({"text": msg}), 200
    return jsonify({"text": "Error: Invalid Key"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
