import time
from ai import *
from spellchecker import SpellChecker
from translate import Translator
import collections
import random
import pyjokes
import requests

import urllib.parse
import subprocess
from bs4 import BeautifulSoup
import json
from ScoolioAPI import *

current_user = None

def translate_to_german(text):
    try:
        translator = Translator(to_lang="de") 
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def get_cat_fact():
    try:
        response = requests.get("https://meowfacts.herokuapp.com/")
        response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
        data = response.json()
        return data.get("data", ["Keine Katzenfakten gefunden"])[0]
    except Exception as e:
        print(f"Fehler beim Abrufen eines Katzenfakts: {e}")
        return "Fehler beim Abrufen eines Katzenfakts."

def get_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=de")
        response.raise_for_status()
        data = response.json()
        return data['text']
    except Exception as e:
        print(f"Fehler beim Abrufen eines Fakts: {e}")
        return "Fehler beim Abrufen eines Fakts."






last_processed_comment = None 

api_key = 'get ur own key, nothing to see here' 

def fetch_image(query):

    # curl-Befehl vorbereiten
    curl_command = [
        'curl',
        '-H', f'Authorization: {api_key}',
        f'https://api.pexels.com/v1/search?query={query}&per_page=1'
    ]

    try:
        # Führe den curl-Befehl aus und speichere die Ausgabe
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        # JSON-Daten aus der Ausgabe laden
        data = json.loads(result.stdout)

        if 'photos' in data and data['photos']:
            # Das erste Bild aus den Ergebnissen zurückgeben
            return data['photos'][0]['src']['original']  # URL des Bildes
        else:
            print("Keine Bilder gefunden.")
            return None
    except Exception as e:
        print(f"Fehler beim Abrufen der Bilder: {str(e)}")
        return None

o = 1

def main():
    global o, last_comment_text, last_processed_comment, current_user
    room = "put in room id here"
    log("your email", "password")


    try:
        while True:

            last_comment_text = check_last_messages(room, 1)
            
            if last_comment_text is None:
                time.sleep(1)  
                continue

            if o == 1:

                message("on", room)
                print(check_last_messages_user(room, 1))
                o = 0

            if last_comment_text.startswith('/q') and last_comment_text != last_processed_comment:
                last_processed_comment = last_comment_text
                question = last_comment_text[2:].strip()  
                response = msg(question)
                if response:
                    try:

                        message(response, room)
                    except Exception as e:
                        print(f"Fehler beim Senden der Antwort auf die Webseite: {e}")
            
            elif last_comment_text.startswith('/r'):
                last_processed_comment = last_comment_text
                text = last_comment_text[3:].strip()
                try:
                    zahl1, zahl2 = map(int, text.split(","))
                    randomzahl = random.randint(zahl1, zahl2)
                except:
                    randomzahl = ">Fehler<   Achte darauf das du ein Leerzeichen zwischen /r und x,y lässt."

                message(randomzahl, room)
                time.sleep(1)
            
            elif last_comment_text.startswith('/help'):
                last_processed_comment = last_comment_text
                helpp = ("-- /q text   --- Generiert KI Antwort  |    /r x,y  --- Gibt eine zufällige Zahl wieder  | "
                         "/specs text  --- Texteigenschaften  |  /joke --- Witz (: | /catfact --- Katzenfakt | "
                         "/fact --- Fakt | /bild query --- Bild zu query  |  /wetter standort --- Wetter abrufen")
                

                message(helpp, room)

                time.sleep(1)
            
            elif last_comment_text.startswith('/joke'):
                last_processed_comment = last_comment_text
                witz = pyjokes.get_joke(language="de")

                message(witz, room)

                time.sleep(1)
            
            elif last_comment_text.startswith('/catfact'):
                last_processed_comment = last_comment_text
                cat_fact = get_cat_fact()
                cat_fact = translate_to_german(cat_fact)

                message(cat_fact, room)

                time.sleep(1)

            elif last_comment_text.startswith('/fact') and last_comment_text != last_processed_comment:
                last_processed_comment = last_comment_text
                fact = get_fact()
  
                message(fact, room)


            if last_comment_text.startswith('/pic') and last_comment_text != last_processed_comment:
                last_processed_comment = last_comment_text
                query = last_comment_text[5:].strip()  # Extrahiere den Suchbegriff nach '/pic'
                
                # Bild abrufen
                image_url = fetch_image(query)
                if image_url:

                    message(image_url, room)
  
                    
            elif last_comment_text.startswith('/wetter') and not last_processed_comment == last_comment_text:
                last_processed_comment = last_comment_text
                location = last_comment_text[8:].strip()  # Extrahiere den Standort nach '/weather'
                access_key = 'your acces key'
                
                # Standort kodieren für URL
                encoded_location = urllib.parse.quote(location)
                
                # Erstelle die API-URL mit dem kodierten Standort
                url = f'http://api.weatherapi.com/v1/current.json?key={access_key}&q={encoded_location}'
                
                try:
                    # Anfrage an WeatherAPI senden
                    response = requests.get(url)
                    response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
                    
                    # JSON-Antwortinhalt auslesen
                    data = response.json()
                    
                    if 'location' in data and 'current' in data:
                        location_name = data['location']['name']
                        temp_c = data['current']['temp_c']
                        condition = data['current']['condition']['text']
                        
                        # Ergebnis in den Chat senden
                        weather_info = f"Das Wetter in {location_name}: {temp_c}°C, {translate_to_german(condition)}."
                        print(weather_info)

                        message(weather_info, room)

                                                
                    else:
                        print("Keine Wetterdaten gefunden.")
                
                except Exception as e:
                    print(f"Fehler bei der API-Anfrage: {str(e)}")
            
            elif last_comment_text.startswith('/calc') and last_comment_text != last_processed_comment:
                last_processed_comment = last_comment_text
                try:
                    expression = last_comment_text[6:].strip()  
                    result = eval(expression)
                    response = f"Ergebnis: {result}"
 
                    message(response, room)

                
                except Exception as e:
                    message("Fehler in der Berechnung. Bitte überprüfe deine Eingabe.", room)
                    
            elif last_comment_text.startswith('/off'):
                if check_last_messages_user(room, 1) == "room id":
                    break

    finally:

        message("Off", room)


if __name__ == "__main__":
    main()