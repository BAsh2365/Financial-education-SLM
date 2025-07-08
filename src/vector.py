from langchain_ollama import OllamaEmbeddings #langchain is a framework for building LLM applications
from langchain_chroma import Chroma #vector DB
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import yfinance as yf

def load_and_chunk_txts(txt_folder, chunk_size=1500, chunk_overlap=300):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    documents = []
    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            path = os.path.join(txt_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                full_text = f.read()
            chunks = splitter.split_text(full_text)
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    documents.append(Document(
                        page_content=chunk,
                        metadata={"source": filename, "chunk": i}
                    ))
    print(f"Loaded {len(documents)} chunks from {txt_folder}")
    return documents

embeddings = OllamaEmbeddings(model="bge-m3")  # Use your installed model name for embedding documents
db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = load_and_chunk_txts("txts")
    ids = [f"{doc.metadata['source']}_{doc.metadata['chunk']}" for doc in documents]

vector_store = Chroma(
    collection_name="company_info",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if not data.empty:
        return float(data["Close"].iloc[-1])
    return None
