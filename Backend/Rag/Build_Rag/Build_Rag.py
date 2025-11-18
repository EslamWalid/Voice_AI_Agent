import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle


nltk.download('punkt_tab')
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def load_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def recursive_split(text, max_words=300):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []

    word_count = 0
    for sent in sentences:
        words_in_sent = len(sent.split())
        if word_count + words_in_sent > max_words:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sent]
            word_count = words_in_sent
        else:
            current_chunk.append(sent)
            word_count += words_in_sent

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

pdf_text = load_pdf(r"E:\Projects\Voice_AI_Agent\Backend\Rag\data\Voice Agent Task.pdf")
print(f"PDF loaded, {len(pdf_text)} characters.")

chunks = recursive_split(pdf_text)
print(f"Recursive splitting produced {len(chunks)} chunks.")

embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

# Normalize for cosine similarity
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
print(f"Embeddings shape: {embeddings.shape}")



dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
index.add(embeddings)

print(f"FAISS index created with {index.ntotal} vectors.")

faiss.write_index(index, "rag_faiss.index")
print("FAISS index saved to rag_faiss.index")

# Save the chunks so we can retrieve text later
with open("rag_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)
print("Chunks saved to rag_chunks.pkl")




def retrieve(query, top_k=3):
    query_vec = model.encode([query], convert_to_numpy=True)
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
    
    # FAISS search
    D, I = index.search(query_vec, top_k)
    
    results = []
    for i, score in zip(I[0], D[0]):
        results.append({"text": chunks[i], "score": float(score)})
    return results



# Test
query = "what is the main objective of the voice AI agent?"
results = retrieve(query, top_k=3)
for r in results:
    print(f"Score: {r['score']:.4f} | Text: {r['text'][:200]}...")