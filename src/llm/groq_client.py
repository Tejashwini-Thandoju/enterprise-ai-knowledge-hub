import os

from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)


def generate_answer(context: str, question: str) -> str:
    """
    Generate an answer using the retrieved context.
    """

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

You must answer ONLY using the information provided in the context.

Rules:
1. Do not make up information.
2. If the answer is not present in the context, reply exactly:
   "I couldn't find this information in the company documents."
3. Keep answers professional and concise.
4. If possible, answer using bullet points.
5. Do not mention that you are an AI model.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content