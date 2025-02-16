import logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the terminal
    ],
)

from urllib.parse import urlencode
import httpx
import pytest
import json
from fastapi import Request
# This termincal command is to run a local server
# poetry run python -m uvicorn src.main:app --reload --log-level info
"""
Use this file for when you're making calls against a running container built with docker.
"""
BASE_URL = "http://127.0.0.1:8000/{endpoint}" # update this if your url is different, you should see it when runing `just run_local`
INDEX = BASE_URL.format(endpoint="")
WEBHOOK_ENDPOINT = BASE_URL.format(endpoint="comment")
PRIVACY_POLICY_ENDPOINT = BASE_URL.format(endpoint="privacy_policy")


def test_uvicorn_container_call():
    with httpx.Client(verify=False) as client:
        response = client.get(
            INDEX,
            timeout=10
        )
    logging.info(f"Response Content: {response.content}")
    assert response.status_code == 200
    assert response.json() == {"status": "Success"} # This is the basic response code set up already

def test_webhook_get():
    query_params = {
        "hub.mode": "subscribe",
        "hub.challenge": "557837336",
        "hub.verify_token": "1234",
    }
    # Encode the query parameters into a URL
    webhook_url = f"{WEBHOOK_ENDPOINT}?{urlencode(query_params)}"
    with httpx.Client(verify=False) as client:
        response = client.get(
            webhook_url,
            timeout=30
        )
    logging.info(f"Response Content: {response.content}")
    assert response.status_code == 200

def test_webhook_post():
    query_params = {
        "hub.mode": "subscribe",
        "hub.challenge": "557837336",
        "hub.verify_token": "1234",
    }
    # Encode the query parameters into a URL
    webhook_url = f"{WEBHOOK_ENDPOINT}?{urlencode(query_params)}"
    with httpx.Client(verify=False) as client:
        response = client.post(
            webhook_url,
            timeout=30
        )
    logging.info(f"Response Content: {response.content}")
    assert response.status_code == 200

def test_privacy_policy():
    with httpx.Client(verify=False) as client:
        response = client.get(
            PRIVACY_POLICY_ENDPOINT,
            timeout=30
        )
    logging.info("I hath returned")
    logging.info(f"Response Content: {response.text}")
    assert response.status_code == 200

def test_send_dm():
    pass