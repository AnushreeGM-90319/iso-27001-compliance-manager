import os
import chromadb

from sentence_transformers import SentenceTransformer

# load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="iso_knowledge_base"
)

DOCS_FOLDER = "docs"

documents = []
ids = []

# read all text files
for index, filename in enumerate(os.listdir(DOCS_FOLDER)):

    if filename.endswith(".txt"):

        filepath = os.path.join(DOCS_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

            documents.append(content)
            ids.append(f"doc_{index}")

# generate embeddings
embeddings = model.encode(documents).tolist()

# store in ChromaDB
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids
)

print("Successfully seeded ChromaDB with 10 documents.")