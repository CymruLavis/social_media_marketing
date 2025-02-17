import logging
from fastapi import Response
import requests
import json

from src.utils.config import settings
import src.codeFiles.openAI_helper as ai

def determine_intent(comment_message:str) -> str:
    intent_to_buy = ai.classify_the_comment(input_message=comment_message)
    return intent_to_buy

def send_message(IGSID: int, IG_ID: int, custom_message:str):
    base_url = f"https://graph.instagram.com/{settings.IG_VERSION}/{IG_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.IG_ACCESS_TOKEN}" , "Content-Type": "application/json"}
    json_body = {
        "recipient": {
            "id": IGSID
        },
        "message":{
            "text": custom_message
        }
    }
    response = requests.post(base_url, headers=headers, json=json_body)
    if response.status_code != 200:
        logging.error(f"Error {response.status_code}: {response.text}")
    else:
        try:
            data=response.json()
            logging.info(json.dumps(data, indent=4))
        except Exception as e:
            logging.error(f"Error decoding JSON response: {e}")
            logging.error(f"Raw Response: {response.text}")


def comment_handler(request: Response):
    logging.info(f"Recieved: {json.dumps(request, indent=4)}")
    
    # Extract relevant fields
    entry = request.get("entry", [])[0]  # Get the first entry
    customers_instagram_id = entry.get("id")
    change = entry.get("changes", [])[0]  # Get the first change
    comment_data = change.get("value", {})
    
    post_id = comment_data.get("media", {}).get("id")
    
    comment_id = comment_data.get("id")
    comment_text = comment_data.get("text")

    sender_instagram_id = comment_data.get("from", {}).get("id")
    sender_instagram_username = comment_data.get("from", {}).get("username")

    intent_to_buy = determine_intent(comment_message=comment_text)
    if intent_to_buy == "yes":
        custom_message = "Create This Later" # query from data base of users products to create a message related to the posted product
        send_message(ISGID=sender_instagram_id, IG_ID=customers_instagram_id, custom_message=custom_message)
    # store comment info in data base
    return "Success"