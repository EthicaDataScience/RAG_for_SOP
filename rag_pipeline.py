import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
#from langchain.embeddings import OpenAIEmbeddings
#from langchain.vectorstores import FAISS


from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI


def load_pdf(file_path):
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_text(text, chunk_size=500, chunk_overlap=50):
    """Split the extracted text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return splitter.split_text(text)

# def load_and_split(file_path):
#     raw_text = load_pdf(file_path)
#     chunks = split_text(raw_text)
#     return chunks

# Updated the load_and_split function to include metadata
def load_and_split(file_path):
    raw_text = load_pdf(file_path)
    chunks = split_text(raw_text)

    # Manually prepend a metadata chunk
    book_metadata = """
    Book Title: Deep Learning from Scratch
    Author: Seth Weidman
    Publisher: O’Reilly Media
    Publication Year: 2019
    """
    chunks.insert(0, book_metadata.strip())
    return chunks



load_dotenv()  # Load API key from .env

def embed_chunks(chunks):
    """Create OpenAI embeddings for each text chunk."""
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

def save_vector_store(vector_store, save_path="vectorstore/faiss_index"):
    """Save the FAISS vector store to disk."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    vector_store.save_local(save_path)


# Accept and run user queries
def load_vector_store(path="vectorstore/faiss_index"):
    return FAISS.load_local(
        path,
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True  # <-- explicit opt-in
    )


def run_query(query, vector_store, k=10):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")  # or "gpt-4"
    
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa.run(query)
    return result

# The following will be used for testing the result with retrieved chunks from the vector store as LLM sees them
# def run_query(query, vector_store, k=10):
#     retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
#     llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
#     docs = retriever.get_relevant_documents(query)
#     print("\n🔎 Retrieved Chunks:\n-------------------------")
#     for i, doc in enumerate(docs):
#         print(f"\nChunk {i+1}:\n{doc.page_content[:500]}...")

#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
#     result = qa.invoke(query)
#     return result

