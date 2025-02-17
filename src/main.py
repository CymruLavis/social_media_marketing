import logging
from typing import Any
logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the terminal
    ],
)

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
import json
import os

from src.codeFiles.response_handler import comment_handler, send_message

# logger = logging.getLogger("my_fastapi_app")

app = FastAPI()

@app.get('/')
def root():
    logging.info("We made it to the root")
    return {"status": "Success"}

@app.route('/privacy_policy')
def privacy_policty(request: Request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "privacy_policy.html")
    with open(file_path, "rb") as f:
        privacy_policty_html = f.read()
    return HTMLResponse(content=privacy_policty_html)

@app.route('/comment', methods=['GET', 'POST'])
async def root(request: Request):
    if request.method == "POST":
        try:
            request_data = await request.json()
            response = comment_handler(request=request_data)
            if response is None:
                logging.warning(f"Unable to handle request: {request_data}")
                return PlainTextResponse(content="FAILURE", status_code=400)

            return PlainTextResponse(content="Success", status_code=200)
        except Exception as e:
            logging.error(f"Error processing POST request: {e}")
            return PlainTextResponse(content="FAILURE", status_code=400)

    if request.method == "GET":
        hub_mode = request.query_params.get('hub.mode')
        hub_challenge = request.query_params.get('hub.challenge')
        hub_verify_token = request.query_params.get('hub.verify_token')

        logging.info("We made it to the comment")

        logging.info(f"Hub Mode: {hub_mode}")
        logging.info(f"Hub Challenge: {hub_challenge}")
        logging.info(f"Hub Verify Token: {hub_verify_token}")

        if hub_challenge:
            logging.info("Verfied")
            logging.info(f"{hub_challenge} is of type {type(hub_challenge)}")
            return PlainTextResponse(content=hub_challenge)  # Echo the hub.challenge value
        else:
            return "<p>Verification Failed</p>"
        
@app.post('/send_dm')
def send_dm(request_data: dict[str,Any]):
    send_message(IGSID=request_data['IGS_ID'], IG_ID=request_data['IG_ID'], custom_message=request_data['custom_message'])
    return PlainTextResponse(content="Success", status_code=200)
