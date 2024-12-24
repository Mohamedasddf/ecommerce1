# paypal.py

import requests
from django.conf import settings

def get_paypal_token():
    url = f"{settings.PAYPAL_API_URL}/v1/oauth2/token"
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET)
    
    response = requests.post(url, headers=headers, data=data, auth=auth)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        return None


def create_payment():
    token = get_paypal_token()
    if not token:
        return None
    
    url = f"{settings.PAYPAL_API_URL}/v1/payments/payment"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    data = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/payment/execute/",  # رابط العودة بعد الدفع
            "cancel_url": "http://127.0.0.1:8000/payment/cancel/"  # رابط الإلغاء
        },
        "transactions": [{
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Test payment"
        }]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        payment = response.json()
        for link in payment['links']:
            if link['rel'] == 'approval_url':
                return link['href']
    else:
        return None


def execute_payment(payment_id, payer_id):
    token = get_paypal_token()
    if not token:
        return None
    
    url = f"{settings.PAYPAL_API_URL}/v1/payments/payment/{payment_id}/execute"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    data = {
        "payer_id": payer_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
