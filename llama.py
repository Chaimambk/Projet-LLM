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

def main():
    context = []
    while True:
        user_input = input("Dis quelque chose : ")
        print()
        context = generate(user_input, context)
        print()

if __name__ == "__main__":
    main()

