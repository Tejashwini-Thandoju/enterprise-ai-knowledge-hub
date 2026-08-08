import os

from groq import Groq
from dotenv import load_dotenv


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Read Groq API Key
# --------------------------------------------------

api_key = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# Create Groq Client
# --------------------------------------------------

client = Groq(api_key=api_key)


# --------------------------------------------------
# Rewrite Follow-up Questions
# --------------------------------------------------

def rewrite_query(question: str, chat_history: list) -> str:
    """
    Convert a follow-up question into a standalone question
    using the previous conversation.
    """

    history_text = ""

    for message in chat_history:
        history_text += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt = f"""
You are a query rewriting assistant for an Enterprise AI
Knowledge Base.

Your task is to rewrite the user's latest question into a
standalone question that can be understood without the
previous conversation.

Rules:

1. Preserve the original meaning.
2. Use the conversation only to resolve references such as
   "it", "they", "that", "what about", etc.
3. Do not answer the question.
4. Do not add information that is not present in the conversation.
5. If the question is already standalone, return it unchanged.
6. Return ONLY the rewritten question.

Conversation:
{history_text}

Latest question:
{question}

Standalone question:
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

    return response.choices[0].message.content.strip()


# --------------------------------------------------
# Generate Grounded Answer
# --------------------------------------------------

def generate_answer(context: str, question: str) -> str:
    """
    Generate an answer using only the retrieved context.
    """

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Your job is to answer the user's question using ONLY the
information provided in the context below.

STRICT RULES:

1. Use only information explicitly stated in the context.

2. Do NOT make assumptions or inferences.

3. Do NOT calculate or derive information that is not explicitly
   stated in the context.

4. Do NOT use your general knowledge.

5. Do NOT invent or hallucinate information.

6. If the exact answer is not explicitly available in the context,
   reply exactly:
   "I couldn't find this information in the company documents."

7. Keep the answer professional and concise.

8. Use bullet points when appropriate.

9. Do not mention that you are an AI model.

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