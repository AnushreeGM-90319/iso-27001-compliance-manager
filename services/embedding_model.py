from sentence_transformers import SentenceTransformer

# preload model at startup
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')