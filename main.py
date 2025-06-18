from rag_pipeline import (
    load_and_split,
    embed_chunks,
    save_vector_store,
    load_vector_store,
    run_query
)
import os

# Directory containing PDFs and path to vector DB
pdf_dir = "data/"
vector_store_path = "vectorstore/faiss_index"

# Check if vector store exists — only embed once
if not os.path.exists(vector_store_path):
    print("🔍 Vector store not found. Running full ingestion + embedding...")
    all_chunks = []
    
    # Iterate through all PDF files in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, filename)
            print(f"📄 Processing: {filename}")
            chunks = load_and_split(file_path)
            all_chunks.extend(chunks)
    
    print(f"✅ Loaded {len(all_chunks)} total chunks from all PDFs.")
    vector_store = embed_chunks(all_chunks)
    save_vector_store(vector_store, vector_store_path)
    print("✅ FAISS index saved to /vectorstore/")
else:
    print("📦 Using existing FAISS index...")

# Load vector store
vector_store = load_vector_store(vector_store_path)

# Interactive query loop
while True:
    query = input("\n🧠 Enter your question (or type 'exit' to quit):\n> ")
    if query.lower() == "exit":
        break
    response = run_query(query, vector_store)
    print("\n📘 Answer:\n", response)
