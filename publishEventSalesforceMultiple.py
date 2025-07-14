import requests
import json
import time
import random
from datetime import datetime

# Config: Replace these with your actual Salesforce credentials
# Config: Replace these with your actual Salesforce credentials and event field details
CLIENT_ID = '3MVG9WVXk15qiz1Ip8cLA53o7y.cvDwWLpl1bV76h6Dp0EJ9Xy3iFyeBfl0YZbKeV3wHdiMyQAd.VGViakc_r'
CLIENT_SECRET = '166D40B55C931EB61F47F08F938926B58912D5A3B1895CBEF26CB12DF9101F11'
USERNAME = 'rohit123pndy@gmail.com'
PASSWORD = 'Qwerty@12435678orcz34g3ccxdtKzQ2HcTbKw2'  # Include security token at the end if required
AUTH_URL = 'https://login.salesforce.com/services/oauth2/token'

# Define event data generators
def generate_order_event():
    return "Order_Confirmed__e", {
        "OrderNumber__c": f"SO{int(time.time())}",
        "CustomerId__c": "CUST00"+str(random.randint(0,999))
    }

def generate_case_event():
    return "Case_Escalated__e", {
        "CaseId__c": f"CASE-{int(time.time())}",
        "Priority__c": "High"
    }

def generate_inventory_event():
    return "Inventory_Threshold_Breached__e", {
        "ProductCode__c": f"PROD-{random.randint(100, 999)}",
        "CurrentStock__c": random.randint(0, 4)
    }

def generate_payment_event():
    return "Payment_Failed__e", {
        "PaymentId__c": f"PMT-{int(time.time())}",
        "CustomerEmail__c": "user@example.com"
    }
    
def generate_Order_Event():
    return "Order_Event__e", {
        "Buyer_Name__c": "CUST00"+str(random.randint(0,999)),
        "Order_Number__c": f"PROD-{random.randint(100, 999)}"
    }

# Randomly choose one event type
def get_random_event():
    event_generators = [
        generate_order_event,
        generate_case_event,
        generate_inventory_event,
        generate_payment_event,
        generate_Order_Event
    ]
    return random.choice(event_generators)()

def get_access_token():
    payload = {
        'grant_type': 'password',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': USERNAME,
        'password': PASSWORD
    }
    response = requests.post(AUTH_URL, data=payload)
    response.raise_for_status()
    data = response.json()
    return data['access_token'], data['instance_url']

def publish_platform_event(access_token, instance_url):
    event_name, payload = get_random_event()
    url = f"{instance_url}/services/data/v60.0/sobjects/{event_name}/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"[{datetime.now()}] Event: {event_name}, Status: {response.status_code}, Response: {response.text}")

def main():
    try:
        access_token, instance_url = get_access_token()
        print("Authenticated successfully.")
        while True:
            publish_platform_event(access_token, instance_url)
            time.sleep(900)
    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    main()