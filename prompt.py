import json
import requests
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel

app = FastAPI()

model_path = "llama3.2:latest"

try:
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print(f"Modèle et tokenizer '{model_path}' chargés avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None
    tokenizer = None

class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 50
    temperature: float = 0.9

def generate(user_input, context):
    r = requests.post(
        'http://127.0.0.1:12346/api/generate',  
        json={
            'model': model_path,  
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

def reponse(prompt, max_length=50, temperature=0.9):
    payload = {
        "prompt": prompt,
        "max_length": max_length,
        "temperature": temperature,
    }

    response = requests.post('http://127.0.0.1:12346/api/generate', json=payload)
    return response.json()["response"]

def main():
    context = []
    while True:
        user_input = input("Dis quelque chose : ")
        print()
        context = generate(user_input, context)
        print()

if __name__ == "__main__":
    main()
