import openai
import requests
from bs4 import BeautifulSoup

# Définir vos clés directement dans le script
OPENAI_API_KEY = "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"

# Configurer l'API OpenAI
openai.api_key = OPENAI_API_KEY

def generer_reponse_ia(question):
    """
    Génère une réponse en utilisant le modèle GPT-3.5 Turbo.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Utilisation du modèle GPT-3.5 Turbo
            messages=[
                {"role": "system", "content": "Tu es un assistant qui répond de manière claire et précise."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        # Renvoyer la réponse générée
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Erreur avec GPT-3.5 Turbo : {e}")
        return None

def rechercher_web(question):
    """
    Recherche une réponse sur le web via DuckDuckGo.
    """
    try:
        # Construire l'URL de recherche DuckDuckGo
        search_url = f"https://html.duckduckgo.com/html/?q={'+'.join(question.split())}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        
        # Effectuer une requête GET
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            return "Impossible d'accéder à DuckDuckGo."

        # Analyser le HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Rechercher les liens des résultats
        results = soup.find_all("a", class_="result__a", limit=1)  # Récupère le premier résultat
        if results:
            # Retourne le texte du lien ou son URL
            return f"Résultat trouvé : {results[0].text}\nLien : {results[0]['href']}"
        else:
            return "Aucun résultat trouvé sur le web."
    except Exception as e:
        print(f"Erreur lors de la recherche web : {e}")
        return "Erreur lors de la recherche web."

def repondre_a_tout(question):
    """
    Tente de répondre à une question en utilisant l'IA, avec une recherche web en secours.
    """
    print("Question posée :", question)
    
    # Essayer de répondre avec l'IA
    reponse = generer_reponse_ia(question)
    
    # Si l'IA ne peut pas répondre ou que la réponse semble vide
    if not reponse or len(reponse.strip()) < 5:
        print("IA incapable de répondre. Recherche sur le web...")
        reponse = rechercher_web(question)
    
    return reponse

if __name__ == "__main__":
    while True:
        question = input("Pose ta question (ou 'quit' pour arrêter) : ")
        if question.lower() in ["quit", "exit", "q"]:
            print("Au revoir !")
            break
        print("Réponse :", repondre_a_tout(question))
