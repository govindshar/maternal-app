import requests

# 🔐 API Key is hardcoded here only — do not share this file publicly
API_KEY = "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"

def query_groq_llm(prompt):
    if not API_KEY:
        return "❌ Groq API key missing."

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "llama3-70b-8192"
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                 headers=headers, json=body, timeout=20)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"
