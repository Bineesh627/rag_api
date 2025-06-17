from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from vector_db.mongodb_manager import MongoDBManager
from sentence_transformers import SentenceTransformer
from rag_engine.prompts import RAG_PROMPT_TEMPLATE 
import numpy as np
import logging
import os
import requests
import time

logger = logging.getLogger(__name__)

class RAGChain:
    def __init__(self):
        logger.info("Initializing RAGChain...")
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(
            os.getenv('EMBEDDING_MODEL_NAME'),
            device='cpu'
        )
        logger.info(f"Loaded embedding model: {self.embedding_model.__class__.__name__}")
        
        # Initialize vector DB
        self.vector_db = MongoDBManager()
        
        # Initialize LLM with retries and validation
        self.llm = self._initialize_llm()
        
        # Create the processing chain
        self.prompt = PromptTemplate(
            template=RAG_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        self.chain = self.prompt | self.llm | StrOutputParser()
        logger.info("RAGChain initialized successfully")

    def _initialize_llm(self, retries=3, delay=2):
        """Initialize Ollama LLM with connection retries and model validation"""
        base_url = os.getenv('OLLAMA_BASE_URL').strip('"\'')
        model_name = os.getenv('LLM_MODEL_NAME')
        
        logger.info(f"Initializing LLM: model={model_name}, base_url={base_url}")
        
        for attempt in range(1, retries + 1):
            try:
                # Verify model is available
                self._verify_ollama_model(base_url, model_name)
                
                # Initialize ChatOllama
                return ChatOllama(
                    model=model_name,
                    temperature=float(os.getenv('LLM_TEMPERATURE')),
                    base_url=base_url,
                    timeout=180  # 3-minute timeout
                )
            except (ConnectionError, ValueError) as e:
                logger.warning(f"LLM initialization attempt {attempt}/{retries} failed: {str(e)}")
                if attempt < retries:
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("LLM initialization failed after all retries")
                    raise

    def _verify_ollama_model(self, base_url, model_name):
        """Check if the specified model exists locally"""
        try:
            url = f"{base_url}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract model names with and without variants
            models = []
            for model in response.json().get('models', []):
                models.append(model['name'])
                # Also consider names without variant qualifiers
                if ':' in model['name']:
                    models.append(model['name'].split(':')[0])
            
            logger.debug(f"Available Ollama models: {models}")
            
            # Check if model is available (exact match or base name)
            if model_name not in models:
                # Try base name match
                base_model = model_name.split(':')[0]
                if base_model in models:
                    logger.info(f"Using base model match: {base_model}")
                    return base_model
                
                available = ", ".join(set(models)) or "None"
                raise ValueError(
                    f"Model '{model_name}' not found in Ollama. "
                    f"Available models: {available}"
                )
            logger.info(f"Verified model exists: {model_name}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Ollama connection failed: {str(e)}. "
                "Make sure Ollama is running: 'ollama serve'"
            ) from e

    def embed_query(self, query):
        """Convert query text to embedding vector"""
        return self.embedding_model.encode(query).tolist()

    def retrieve_context(self, query_embedding, top_k=5):
        """Retrieve top_k most relevant document chunks"""
        return self.vector_db.cosine_similarity_search(query_embedding, top_k=top_k)

    def format_context(self, context_results):
        """Format context for the prompt"""
        return "\n\n".join([f"• {res['text']}" for i, res in enumerate(context_results)])

    def generate(self, query, top_k=3):
        """Generate response to user query"""
        try:
            logger.info(f"Processing query: {query[:50]}...")
            
            # Embed query
            query_embedding = self.embed_query(query)
            logger.debug("Query embedded successfully")
            
            # Retrieve context
            context_results = self.retrieve_context(query_embedding, top_k=top_k)
            logger.info(f"Retrieved {len(context_results)} context chunks")
            
            if not context_results:
                logger.warning("No context retrieved for query")
                return "I couldn't find relevant information to answer this question.", []
            
            formatted_context = self.format_context(context_results)
            logger.debug(f"Formatted context: {formatted_context[:100]}...")
            
            # Generate response
            response = self.chain.invoke({
                "context": formatted_context,
                "question": query
            })
            logger.info("Generated LLM response successfully")
            
            return response, [res.get('metadata', {}) for res in context_results]
        
        except Exception as e:
            logger.exception("RAG generation failed")
            return "I encountered an error processing your request. Please try again later.", []