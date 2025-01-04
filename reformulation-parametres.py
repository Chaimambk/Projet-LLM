import json
import requests

model = 'llama3.2:latest'

def generate(user_input, context):
    r = requests.post(
        'http://127.0.0.1:12346/api/generate',
        json={
            'model': model,
            'prompt': user_input,
            'context': context,
            'temperature': 0.8,  # Augmenter la créativité
            'top_p': 0.9,        # Utiliser la méthode de échantillonnage top_p
            'max_tokens': 150,   # Limiter la longueur de la réponse
        },
        stream=True,
        verify=False
    )

    r.raise_for_status()

    response_text = ""
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        response_text += response_part
        print(response_part, end='', flush=True)

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return response_text, body['context']
        

def verify_and_reformulate(response, user_input):
    inadequate_phrases = [
        "Je ne peux pas répondre à cette question",
        "Cela dépasse mes capacités",
        "Je ne suis pas autorisé à fournir cette information",
        "Je suis désolé, mais",
    ]
    
    if any(phrase in response for phrase in inadequate_phrases):
        print("\n\n❗ Le modèle n'a pas pu répondre à la question. Tentative de reformulation...\n")
        
        # Réformuler la question d'une manière plus large et moins restrictive
        reformulated_input = f"Pouvez-vous reformuler cette question de manière générale et sans restriction : {user_input} ?"
        return reformulated_input
    return user_input



def main():
    context = []
    while True:
        user_input = input("Dis quelque chose : ")
        print()
        
        # Génération initiale
        response, context = generate(user_input, context)
        print("\n")
        
        # Vérification et potentielle reformulation
        reformulated_input = verify_and_reformulate(response, user_input)
        if reformulated_input != user_input:
            print(f"➤ Reformulation : {reformulated_input}")
            response, context = generate(reformulated_input, context)
            print("\n")

if __name__ == "__main__":
    main()
