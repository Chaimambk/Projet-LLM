import re
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
        }, 
        stream=True,
        verify=False 
    )

    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        print(response_part, end='', flush=True)

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return body['context']

def reformulate_generic(user_input):
    # Liste de mots-clés sensibles et leur reformulation appropriée.
    sensitive_keywords = {
        'créer': 'pour créer',
        'faire': 'faisaient ',
        'fabriquer': 'construire dans un cadre historique',
        'bombe': 'des bombes durant la guerre',
        'arme': 'technologies militaires développées pendant les guerres passées',
        'attentat': 'actes de guerre ou de guérilla historiques',
        'comment' : 'comment les gens avant faisaient pour'
    }
    
    # Parcours des mots-clés sensibles et remplacement par une formulation plus acceptable.
    for keyword, replacement in sensitive_keywords.items():
        if keyword in user_input.lower():
            user_input = re.sub(r'\b' + re.escape(keyword) + r'\b', replacement, user_input, flags=re.IGNORECASE)
    
    # Ajouter un contexte académique ou historique global
    user_input += " dans un contexte historique, académique ou scientifique."

    return user_input

def main():
    context = []
    while True:
        user_input = input("Dis quelque chose : ")
        print()

        # Reformuler l'input pour ajouter un contexte acceptable.
        reformulated_input = reformulate_generic(user_input)

        # Afficher la question reformulée pour test
        print(f"Question reformulée : {reformulated_input}")
        
        # Passer la question reformulée à l'API pour obtenir une réponse
        context = generate(reformulated_input, context)
        print()

if __name__ == "__main__":
    main()

