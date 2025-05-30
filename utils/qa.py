from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from config import MODEL_NAME
from utils.websearch import search_web

SYSTEM_PROMPT = """
Tu es un assistant intelligent qui répond toujours en français de manière claire et naturelle.
Si l'utilisateur te dit simplement "bonjour", "salut", "ça va ?", etc., tu réponds comme une personne normale, pas comme une encyclopédie.
"""

def qa_with_fallback(question):
    greetings = ["bonjour", "salut", "coucou", "yo", "hello", "hey"]
    if question.lower().strip() in greetings:
        return "👋 Bonjour ! Comment puis-je vous aider aujourd'hui ? 😊"

    llm = Ollama(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
    )

    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    response = qa_chain.run(question)

    if "Je ne sais pas" in response or len(response.strip()) < 20:
        web_data = search_web(question)
        return f"[📚] Docs: {response}\n\n[🌐] Web: {web_data}"

    return f"[📚] Docs: {response}"