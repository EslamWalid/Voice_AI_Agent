# Voice AI Agent (LiveKit + Gemini Live API + RAG)

This project implements a real-time voice AI agent using LiveKit, Google
Gemini Live API, and a custom RAG pipeline.

## 🚀 Project Overview

This project integrates: - LiveKit for audio streaming - Gemini Live API
for live LLM responses - RAG for document-based knowledge retrieval -
React frontend for user interaction - Python backend for agent logic

## 📂 Repository Structure

    .
├── Backend/                          # Python backend (agent, RAG, token server)
│   ├── agent.py                      # LiveKit agent entrypoint (AgentSession + tools)
│   ├── .env                          # Backend environment variables (local only)
│   ├── requirements.txt              # Python deps
│   ├── Tokens_generator/             # Simple token service for frontend
│   │   └── server.py                 # Flask endpoint: /getToken
│   └── Rag/                          # RAG pipeline and built index
│       ├── Rag.py                    # Retrieval API used by agent
│       ├── rag_faiss.index           # FAISS index (binary)
│       ├── rag_chunks.pkl            # Serialized text chunks (used by rag.py)
│       ├── Build_Rag/                # RAG build utilities
│       │   └── Build_Rag.py
│       └── data/                     # Source documents for RAG (pdfs, txt)
│           └── Voice Agent Task.pdf
│
├── livekit-frontend/                 # React frontend (LiveKit client)
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js
|       .    
│       .               
│       .                
│       └── setupTests.js                      
| 
├── demo/                             
│   └── demo.mp4           
└── README.md

## ⚙️ Setup Instructions

### Clone the repo

    git clone https://github.com/EslamWalid/Voice_AI_Agent.git
    cd Voice_AI_Agent

## 🔑 Environment Variables

### Backend `.env`

    LIVEKIT_API_KEY=your_livekit_key
    LIVEKIT_API_SECRET=your_livekit_secret
    GEMINI_API_KEY=your_gemini_api_key
    EMBEDDING_MODEL=text-embedding-004
    



## 🧰 Backend Setup

    cd Backend
    pip install -r requirements.txt
    python agent.py download-files
    python agent.py start


### Variables Setup

#### Token:
    cd Backend/Tokens_generator
    python server.py

##### go to http://127.0.0.1:5000/getToken
##### copy token
##### open livekit-frontend\src\App.js and put it in:
    const token = ""

#### URL 

##### go to .env
##### copy LIVEKIT_URL
##### open livekit-frontend\src\App.js and put it in:
    const serverUrl = ""

## 💻 Frontend Setup

    cd livekit-frontend
    npm install
    npm start

## 🧱 Architecture Overview

-   LiveKit handles audio streaming
-   Python agent streams audio to Gemini
-   RAG retrieves relevant chunks from FAISS
-   Gemini uses retrieved context via tool calling

## ▶️ Running the System

1.  Start backend
2.  Start frontend
3.  Speak → Get real-time AI responses

## 🎥 Demo

Place demo file in `demo/demo.mp4`.

## 🧾 RAG + Gemini Integration

RAG retrieval is injected via a function tool exposed to Gemini.

## 🙋 Support

Check: - NLTK installation - Environment variables - FAISS path -
LiveKit server URL
