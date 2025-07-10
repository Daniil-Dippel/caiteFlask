from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

HF_TOKEN = "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"
MODEL = "tiiuae/falcon-7b-instruct"  # стабильная модель

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get("messages", [])

    # Сборка диалога
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

        # Проверка: правильный ли ответ
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
