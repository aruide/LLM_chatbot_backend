import os
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader, UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import MODEL_NAME
from utils.websearch import search_web

SYSTEM_PROMPT = """
Tu es un assistant intelligent qui répond toujours en Français de manière claire et naturelle. 
Ignore complètement les emoji dans les messages : ne les lis pas, ne les commente pas, ne les utilise pas dans tes réponses.
Si l'utilisateur écrit juste "bonjour", "salut", "ça va ?", etc., tu réponds de façon simple et naturelle, comme une personne normale, pas comme une encyclopédie.
"""

# Chargement et indexation des documents
def load_vector_store():
    loaders = [
        DirectoryLoader("documents", glob="**/*.txt", loader_cls=TextLoader),
        DirectoryLoader("documents", glob="**/*.pdf", loader_cls=UnstructuredPDFLoader),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore

def qa_with_fallback(question):
    greetings = ["bonjour", "salut", "coucou", "yo", "hello", "hey"]
    if question.lower().strip() in greetings:
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"

    llm = Ollama(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        base_url="http://host.docker.internal:11434"
    )
    
    # Vérifier dans les documents
    vectorstore = load_vector_store()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

    local_response = qa_chain.run(question)

    # Si la réponse est pauvre ou peu pertinente, faire une recherche web
    if "Je ne sais pas" in local_response or len(local_response.strip()) < 20:
        return search_web(question)

    return local_response