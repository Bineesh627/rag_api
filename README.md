```markdown
# RAG Chatbot API with Django & Ollama

![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![Ollama](https://img.shields.io/badge/ollama-llama3-orange)

A Retrieval-Augmented Generation (RAG) chatbot API built with Django REST Framework and Ollama, featuring document retrieval from MongoDB and local LLM inference.

## ✨ Features

- **Local LLM Processing**: Uses Ollama with llama3 model for response generation
- **Semantic Search**: SentenceTransformer embeddings with FAISS-based similarity search
- **Modular Architecture**:
  - Separate components for API, RAG engine, vector DB, and chat history
- **Production-Ready**:
  - Environment variable configuration
  - Comprehensive error handling
  - Request validation
  - Performance monitoring
- **Extensible Design**:
  - Easy to swap LLM providers
  - Support for multiple vector databases
  - Customizable prompt templates

## 🚀 Quick Start

### Prerequisites
- Python 3.12
- MongoDB (local or Atlas)
- Ollama with at least one model (e.g., `llama3`)

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Configuration
Create `.env` file:
```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=rag_db
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
LLM_TEMPERATURE=0.7
```

### Running the API
```bash
# Start Django development server
python manage.py runserver

# In another terminal, start Ollama
ollama serve
```

## 📚 API Documentation

### POST `/api/query/`
Submit a query to the chatbot.

**Request:**
```json
{
  "query": ["your question or message"],
  "session_id": "optional-session-id"
}
```

**Successful Response (200):**
```json
{
  "query": ["your original question"],
  "response": ["generated answer"],
  "sources": [
    {
      "text": "retrieved document chunk",
      "metadata": {
        "source": "document.pdf",
        "page": 3
      }
    }
  ]
}
```

## 🛠️ Project Structure

```
rag_project/
├── core/                  # Django project settings
├── api/                   # REST API endpoints
├── rag_engine/            # LangChain processing
├── vector_db/             # Vector similarity search
├── chat_history/          # Conversation logging
├── model_config/          # LLM configuration
├── manage.py
├── requirements.txt
└── .env
```

## 🔧 Customization

### Changing LLM Model
Edit `.env`:
```env
LLM_MODEL_NAME=mistral  # or other Ollama model
```

### Modifying Prompts
Edit `rag_engine/prompts.py`:
```python
CUSTOM_PROMPT = """
You are a helpful assistant. Use this context:

{context}

Question: {question}

Answer concisely:
"""
```

## 🤖 Testing
Run the test suite:
```bash
python manage.py test
```

Test with curl:
```bash
curl -X POST http://localhost:8000/api/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": ["How does this work?"]}'
```

## 📈 Performance Optimization

For better performance:
1. Use GPU acceleration (set `device=cuda` in embedding model)
2. Implement caching for embeddings
3. Add indexes to MongoDB collections
4. Use smaller embedding models for faster inference

## 📜 License
MIT License - See [LICENSE](LICENSE) for details

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

---

💡 **Tip**: For production deployment, consider using:
- Gunicorn + Nginx
- Docker containers
- Redis caching
- Proper secret management
```
