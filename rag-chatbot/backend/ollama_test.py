
from ollama import chat

response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant specialising in machine learning and artificial intelligence."
        },
        {
            "role": "user",
            "content": "Explain Retrieval-Augmented Generation (RAG) in three simple sentences."
        }
    ]
)

print(response.message.content)
