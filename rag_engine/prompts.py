RAG_PROMPT_TEMPLATE = """
You are an expert assistant. Use the following context to answer the question. 
If you don't know the answer, just say you don't know. Be concise and accurate.

Context:
{context}

Question: {question}

Answer:
"""