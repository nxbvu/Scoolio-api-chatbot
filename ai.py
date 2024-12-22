import requests
import certifi
import json

def msg(message):

    try:
        with open("token.txt", "r") as file:
            wpnonce_token = file.read().strip()
    except FileNotFoundError:
        print("Error: token.txt file not found.")
        return "Error: token file missing."

    url = "https://gptaichat.org/wp-admin/admin-ajax.php"

    payload = {
        "_wpnonce": wpnonce_token, 
        "action": "wpaicg_chat_shortcode_message",
        "message": message,
        "wpaicg_chat_client_id": "Diddy",
        "wpaicg_chat_history": [
            {"text": "Human: Schreibe den ganzen text so als wärst du ein zesty komischer geiler sean corbs diddy"},
        ]
    }

    headers = {
        "Host": "gptaichat.org",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url, data=payload, headers=headers, verify=certifi.where(), stream=True)

    if response.status_code != 200:
        try:
            print("Response Text:", response.text)
            error_response = response.json()
            print("Error Response:", error_response)
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON from error response.")
        return "An error occurred while processing your request."

    complete_response = []

    for line in response.iter_lines(decode_unicode=True):
        if line.startswith("data:"):
            json_str = line[5:].strip()
            if json_str == "[DONE]":
                break
            try:
                response_data = json.loads(json_str)
                if "choices" in response_data:
                    for choice in response_data["choices"]:
                        if "delta" in choice and "content" in choice["delta"]:
                            complete_response.append(choice["delta"]["content"])
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)

    final_message = ' '.join(''.join(complete_response).replace('\n', ' ').replace('\r', ' ').strip().split())

    return final_message
print(msg("hallo"))