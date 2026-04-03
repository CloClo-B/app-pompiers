# fichier pour la validation du captcha cloudflare récuperer durectement depuis la doc officiel
import requests
from fastapi import APIRouter, Request, Form
import os


# Charger la clé depuis .env

# clé de TEST UNIQUEMENT a changer pour la production
SECRET_KEY = os.getenv("CLE_CAPTCHA")

router = APIRouter()


def valider_turnstile(token, secret, remoteip=None):
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    data = {'secret': secret, 'response': token}
    if remoteip:
        data['remoteip'] = remoteip
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Turnstile validation error: {e}")
        return {'success': False, 'error-codes': ['internal-error']}


@router.post('/submit-form')
async def register(request: Request, cf_turnstile_response: str = Form(alias="cf-turnstile-response")):
    remoteip = request.headers.get('CF-Connecting-IP') or \
               request.headers.get('X-Forwarded-For') or \
               request.client.host

    validation = valider_turnstile(cf_turnstile_response, SECRET_KEY, remoteip)
    
    # renvoie erreur si non valide
    if not validation['success']:
        return {'status': 'error', 'errors': validation['error-codes']}
   
    # renvoie success si ok
    return {'status': 'success'}