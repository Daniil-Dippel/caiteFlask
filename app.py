from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Вставьте свой токен Hugging Face сюда
HF_TOKEN = "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"

# Используем модель Mistral (или другую — можно заменить)
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get("messages", [])

    # Собираем промпт
    prompt = (
        "Ты — Фелис, ИИ-помощник компании ЦАИТО МУИТ. "
        "Отвечай на русском языке, кратко, дружелюбно и по делу. "
        "Не выдумывай фактов. Ты создана командой ЦАИТО МУИТ. "
    )

    for msg in messages:
        role = "Пользователь" if msg["speaker"] == "user" else "Фелис"
        prompt += f"\n{role}: {msg['text']}"
    prompt += "\nФелис:"

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt},
            timeout=30
        )

        result = response.json()
        if isinstance(result, list):
            text = result[0].get("generated_text", "")
            answer = text.split("Фелис:")[-1].strip()
        else:
            answer = "Ошибка: ответ от модели не в нужном формате."

    except Exception as e:
        answer = f"Ошибка при подключении: {e}"

    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)