from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from config import MODEL_NAME
from utils.websearch import search_web

SYSTEM_PROMPT = """
Tu es un assistant intelligent qui répond toujours en Français de manière claire et naturelle. 
Ignore complètement les emoji dans les messages : ne les lis pas, ne les commente pas, ne les utilise pas dans tes réponses.
Si l'utilisateur écrit juste "bonjour", "salut", "ça va ?", etc., tu réponds de façon simple et naturelle, comme une personne normale, pas comme une encyclopédie.
"""

def qa_with_fallback(question):
    greetings = ["bonjour", "salut", "coucou", "yo", "hello", "hey"]
    if question.lower().strip() in greetings:
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"

    llm = Ollama(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        base_url="http://host.docker.internal:11434"
    )

    response = llm(question)

    if "Je ne sais pas" in response or len(response.strip()) < 20:
        web_data = search_web(question)
        return web_data

    return response