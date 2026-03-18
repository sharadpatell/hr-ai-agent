from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
import os
import re


def retrieve(query):

    print("\n🔍 RETRIEVER STARTED\n")

    # 🔥 check DB exists
    if not os.path.exists("data/vector_db"):
        print("❌ chroma_db not found")
        return []

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = Chroma(
        persist_directory="data/vector_db",
        embedding_function=embeddings
    )

    # 🔥 Source filtering based on query
    source_map = {
        "simplilearn": "simplilearn_com.txt",
        "interviewbit": "interviewbit_com.txt",
        "geeksforgeeks": "geeksforgeeks_org.txt",
        "indeed": "indeed_com.txt",
        "indiabix": "indiabix_com.txt",
        "hibob": "hibob_com.txt",
        "gsdcouncil": "gsdcouncil_org.txt",
        "fita": "fita_in.txt",
        "themuse": "themuse_com.txt",
        "prepinsta": "prepinsta_com.txt",
        "naukri": "naukri_com.txt",
        "linkedin": "linkedin_com.txt"
    }
    filter_dict = None
    for key, source in source_map.items():
        if key in query.lower():
            filter_dict = {"source": source}
            print(f"🔍 Filtering by source: {source}")
            break

    # 🔥 Get all docs for BM25 and filtering
    all_docs = db.get()
    documents = all_docs["documents"]
    metadatas = all_docs["metadatas"]
    ids = all_docs["ids"]

    # 🔥 Filter docs if source specified
    if filter_dict:
        filtered_indices = [i for i, meta in enumerate(metadatas) if meta.get("source") == filter_dict["source"]]
        documents = [documents[i] for i in filtered_indices]
        metadatas = [metadatas[i] for i in filtered_indices]
        ids = [ids[i] for i in filtered_indices]

    # 🔥 BM25 Retriever for keyword matching
    bm25_retriever = BM25Retriever.from_texts(documents, metadatas=metadatas)

    # 🔥 Vector Retriever with MMR
    vector_retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "lambda_mult": 0.5,
            "filter": filter_dict
        }
    )

    # 🔥 Get docs from both retrievers
    bm25_docs = bm25_retriever.invoke(query)
    vector_docs = vector_retriever.invoke(query)

    # 🔥 Combine and deduplicate (simple ensemble simulation)
    all_docs = bm25_docs + vector_docs
    seen = set()
    docs = []
    for doc in all_docs:
        if doc.page_content not in seen:
            docs.append(doc)
            seen.add(doc.page_content)
        if len(docs) >= 5:
            break

    # 🔥 Deduplicate docs
    seen = set()
    unique_docs = []
    for doc in docs:
        if doc.page_content not in seen:
            unique_docs.append(doc)
            seen.add(doc.page_content)
        if len(unique_docs) >= 5:
            break

    print(f"📊 Retrieved {len(unique_docs)} unique documents\n")

    context = []

    for i, doc in enumerate(unique_docs):
        print(f"\n--- CHUNK {i+1} ---")
        print(f"SOURCE: {doc.metadata.get('source')}")
        print(doc.page_content[:300])

        context.append(doc.page_content)

    return context