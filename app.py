from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from cryptography.fernet import Fernet

app = Flask(__name__)
CORS(app)

# Ваш ключ и зашифрованный токен
key_str = "mMVhYfzITdAWDzwwts5Mgpf1ls_FNAfdDCtsuxsUkfI="
encrypted_token_str = "gAAAAABob8xh3ZdCXPRcH4EpdrMOZKbP19qjYcREtRVEgtgM3n1salesYTILG9_HkW7qBhGjKIQAmDjyUD8ypexUcwqs7lbtpvx2oIBsNqhl_bNOVndYzf_bGaIRIRxwqY44k-llVCoH"

# Расшифровка токена
cipher = Fernet(key_str.encode())
decrypted_token = cipher.decrypt(encrypted_token_str.encode())
HF_TOKEN = decrypted_token.decode()

MODEL = "tiiuae/falcon-7b-instruct"  # стабильная модель

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get("messages", [])

    prompt = (
        "Ты — Фелис, ИИ-помощник компании ЦАИТО МУИТ. "
        "Отвечай на русском языке, дружелюбно, кратко и по делу.\n"
    )
    for msg in messages:
        role = "Пользователь" if msg["speaker"] == "user" else "Фелис"
        prompt += f"{role}: {msg['text']}\n"
    prompt += "Фелис:"

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt},
            timeout=30
        )

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            full_text = result[0]["generated_text"]
            answer = full_text.split("Фелис:")[-1].strip()
        elif isinstance(result, dict) and "error" in result:
            answer = f"Ошибка Hugging Face: {result['error']}"
        else:
            answer = "Не удалось распознать ответ модели."

    except Exception as e:
        answer = f"Ошибка при запросе: {e}"

    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)
