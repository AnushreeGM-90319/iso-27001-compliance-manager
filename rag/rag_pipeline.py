import os
from sentence_transformers import SentenceTransformer
import chromadb

# -------------------------------
# STEP 1: Load Documents
# -------------------------------
def load_documents(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------
# STEP 2: Chunk Text (500 chars, 50 overlap)
# -------------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# -------------------------------
# STEP 3: Create Embeddings
# -------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):
    return model.encode(chunks)


# -------------------------------
# STEP 4: Store in ChromaDB
# -------------------------------
def store_in_chroma(chunks, embeddings):
    # Create persistent DB
    client = chromadb.Client(
    chromadb.config.Settings(persist_directory="chroma_db")
)

    # Create collection
    collection = client.create_collection(name="rag_collection")

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i].tolist()],
            ids=[str(i)]
        )

    return collection


# -------------------------------
# MAIN PIPELINE
# -------------------------------
if __name__ == "__main__":
    print("🚀 Starting RAG Pipeline...")

    # Load
    text = load_documents("data/documents.txt")

    # Chunk
    chunks = chunk_text(text)
    print(f"✅ Created {len(chunks)} chunks")

    # Embeddings
    embeddings = create_embeddings(chunks)
    print("✅ Embeddings created")

    # Store
    collection = store_in_chroma(chunks, embeddings)
    print("✅ Stored in ChromaDB")

    print("🎉 RAG pipeline completed successfully!")