import faiss
import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Rag.py folder
index_path = os.path.join(BASE_DIR, "rag_faiss.index")
chunks_path = os.path.join(BASE_DIR, "rag_chunks.pkl")

# Load index
index = faiss.read_index(index_path)

# Load chunks
with open(chunks_path, "rb") as f:
    chunks = pickle.load(f)

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
print("RAG components loaded successfully.")
# Example retrieval function
def retrieve(query, top_k=3):
    query_vec = model.encode([query], convert_to_numpy=True)
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
    D, I = index.search(query_vec, top_k)
    return [{"text": chunks[i], "score": float(D[0][j])} for j, i in enumerate(I[0])]

# Test retrieval
# results = retrieve("what is the Requirments")
# for r in results:
#     print(f"Score: {r['score']:.4f} | Text: {r['text'][:]}...")
