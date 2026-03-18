import os
from datetime import datetime
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_PATH = "data/raw"
VECTOR_DB_PATH = "data/vector_db"
LOG_FILE = "logs/embedding.log"


def log(msg):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {msg}\n")


def load_files():
    docs = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                text = f.read()

                docs.append({
                    "content": text,
                    "source": file
                })

                log(f"Loaded: {file}")

    return docs


def chunk_data(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Increased for better context
        chunk_overlap=200  # Increased overlap for continuity
    )

    chunks = []

    seen = set()  # To deduplicate chunks

    for doc in docs:
        splits = splitter.split_text(doc["content"])

        for chunk in splits:
            if chunk not in seen:
                chunks.append({
                    "content": chunk,
                    "source": doc["source"]
                })
                seen.add(chunk)

    log(f"Total unique chunks: {len(chunks)}")

    return chunks


def create_embeddings(chunks):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    texts = [c["content"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=VECTOR_DB_PATH
    )

    log("Embeddings created and stored")


if __name__ == "__main__":
    docs = load_files()
    chunks = chunk_data(docs)
    create_embeddings(chunks)

    print("✅ Embedding complete")