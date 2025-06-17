import os
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logger = logging.getLogger(__name__)

class MongoDBManager:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URI')
        self.db_name = os.getenv('MONGODB_DB_NAME')
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db['document_chunks']
        logger.info(f"Connected to MongoDB: {self.db_name}")

    def cosine_similarity_search(self, query_embedding, top_k=5):
        try:
            # Get all chunks with embeddings
            chunks = list(self.collection.find({}, {'embedding': 1, 'text': 1, 'metadata': 1}))
            
            if not chunks:
                return []
            
            # Extract embeddings and calculate similarities
            embeddings = [np.array(chunk['embedding']) for chunk in chunks]
            similarities = cosine_similarity([query_embedding], embeddings)[0]
            
            # Get top K results
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            results = [{
                'text': chunks[i]['text'],
                'metadata': chunks[i].get('metadata', {}),
                'score': float(similarities[i])
            } for i in top_indices]
            
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            raise