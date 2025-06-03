from langchain.llms import Ollama
from utils.websearch import search_web

MODEL_NAME = "llama3"  # ou llama3, gemma, etc.

SYSTEM_PROMPT = """
Tu es un assistant intelligent qui répond toujours en Français de manière claire et naturelle. 
Ignore complètement les emoji dans les messages : ne les lis pas, ne les commente pas, ne les utilise pas dans tes réponses.
Si l'utilisateur écrit juste "bonjour", "salut", "ça va ?", etc., tu réponds de façon simple et naturelle, comme une personne normale, pas comme une encyclopédie.
"""

llm = Ollama(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        base_url="http://host.docker.internal:11434"
    )

def qa_with_fallback(question):
    greetings = ["bonjour", "salut", "coucou", "yo", "hello", "hey"]
    if question.lower().strip() in greetings:
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    
    local_response = llm(question)

    # Si la réponse est pauvre ou peu pertinente, faire une recherche web
    if "Je ne sais pas" in local_response or len(local_response.strip()) < 20:
        return search_web(question)

    return local_response