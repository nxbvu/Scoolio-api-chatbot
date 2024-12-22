import requests
import certifi
import pandas as pd
from datetime import datetime

token = None

def log(user, password):
    global token
    url_login = "https://userbridge.services.scoolio.de/v1/login/identifier"
    data_login = {
        "Identifier": user,
        "Secret": password
    }

    print("Attempting to log in with user:", user)
    response_login = requests.post(url_login, json=data_login, verify=certifi.where())


    response_data = response_login.json()
    print("Login Response Data:", response_data)

    token = response_data.get('Result', {}).get('Token')
    current_user = response_data.get('User', {}).get('UserID')

    print("Current User:", current_user)


def message(message, room):
    global token
    url_send_message = f"https://chat.services.scoolio.de/v1/rooms/{room}/messages"
    message_data = {
        "Type": "text",
        "Content": message
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Length": str(len(str(message_data))), 
        "x-scoolio-csrf": "1", 
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "host": "chat.services.scoolio.de"
    }

    print("Sending message to room:", room)
    print("Message Data:", message_data)
    print("Headers:", headers)

    try:
        rr = requests.post(url_send_message, json=message_data, headers=headers, verify=certifi.where())

        print("Response Text:", rr.text)

        if rr.status_code != 200:
            print("Error in request. Please check the URL, headers, and data.")
    except requests.exceptions.RequestException as e:
        print("Error sending the request:", e)

def check_last_messages_fine(room, anzahl):
    global token
    url_last_messages = f"https://chat.services.scoolio.de/v1/rooms/{room}/messages?LastN={anzahl}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "x-scoolio-csrf": "1",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "host": "chat.services.scoolio.de"
    }

    print("Checking last messages in room:", room)
    print("Requesting last N messages:", anzahl)
    print("URL for last messages:", url_last_messages)

    try:
        response = requests.get(url_last_messages, headers=headers, verify=certifi.where())


        if response.status_code == 200:
            data = response.json()
            print("Response Data:", data)
            messages = data.get('Result', {}).get('Items', [])
            
            # Prepare data for return
            message_data = []
            for message in messages:
                user_id = message['Author']['ID']
                user_name = message['Author']['Name']
                content = message['Content']
                timestamp = datetime.fromtimestamp(message['SentAt']).strftime('%Y-%m-%d %H:%M:%S')
                
                message_data.append({
                    "UserID": user_id,
                    "User": user_name,
                    "Nachricht": content,
                    "Zeit": timestamp
                })
                print("Extracted Message:", message_data[-1])  
            
    
            print(message_data)
            return message_data
            
        else:
            print("Error in request. Please check the URL, headers, and data.")
            return None 

    except requests.exceptions.RequestException as e:
        print("Error sending the request:", e)
        return None 
    
    
def check_last_messages(room, anzahl):
    global token
    url_last_messages = f"https://chat.services.scoolio.de/v1/rooms/{room}/messages?LastN={anzahl}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "x-scoolio-csrf": "1",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "host": "chat.services.scoolio.de"
    }

    try:
        response = requests.get(url_last_messages, headers=headers, verify=certifi.where())

        if response.status_code == 200:
            data = response.json()
            messages = data.get('Result', {}).get('Items', [])
            
            if messages:

                last_message = messages[0]
                content = last_message['Content']
                return content  # Gib nur den Content zurück
            
            else:
                print("Keine Nachrichten gefunden.")
                return None  

        else:
            print("Fehler bei der Anfrage. Bitte überprüfe die URL, die Headers und die Daten.")
            return None  

    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Anfrage:", e)
        return None  

def check_last_messages_user(room, anzahl):
    global token
    url_last_messages = f"https://chat.services.scoolio.de/v1/rooms/{room}/messages?LastN={anzahl}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "x-scoolio-csrf": "1",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "host": "chat.services.scoolio.de"
    }

    try:
        response = requests.get(url_last_messages, headers=headers, verify=certifi.where())


        if response.status_code == 200:
            data = response.json()
            messages = data.get('Result', {}).get('Items', [])
            print(messages)
            
            if messages:

                last_message = messages[0]
                author_id = last_message.get('Author', {}).get('ID')
                print("Extracted Author ID:", author_id)  
                return author_id  # Gib nur die ID des Authors zurück
            
            else:
                print("Keine Nachrichten gefunden.")
                return None  

        else:
            print("Fehler bei der Anfrage. Bitte überprüfe die URL, die Headers und die Daten.")
            return None 
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Anfrage:", e)
        return None  
# Beispielaufruf 
# check_last_messages_user("2b2cf9f2-420a-4b3b-8361-3c1cab7c077c", 1)


# Last messages
# check_last_messages("2b2cf9f2-420a-4b3b-8361-3c1cab7c077c", 100)
