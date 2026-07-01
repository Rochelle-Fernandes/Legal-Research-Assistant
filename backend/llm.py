import requests

MODEL_URL = "http://127.0.0.1:9000/v1/chat/completions"


def generate_answer(context, question):

    prompt = f"""
You are a Legal Research Assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:
"I couldn't find that information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    payload = {
        "model": "qwen",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(
            MODEL_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        return answer

    except requests.exceptions.ConnectionError:
        return (
            "❌ Could not connect to the local LLM server.\n\n"
            "Please start llama.cpp and try again."
        )

    except requests.exceptions.Timeout:
        return (
            "❌ The LLM server took too long to respond."
        )

    except requests.exceptions.RequestException as e:
        return (
            f"❌ Request failed:\n{e}"
        )

    except KeyError:
        return (
            "❌ Unexpected response received from the LLM server."
        )