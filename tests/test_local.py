import httpx
import pytest
import logging
import json

# This termincal command is to run a local server
# poetry run python -m uvicorn src.main:app --reload --log-level info
"""
Use this file for when you're making calls against a running container built with docker.
"""
BASE_URL = "http://127.0.0.1:8000/{endpoint}" # update this if your url is different, you should see it when runing `just run_local`
INDEX = BASE_URL.format(endpoint="")
WEBHOOK_ENDPOINT = BASE_URL.format(endpoint="comment")


def test_uvicorn_container_call():
    with httpx.Client(verify=False) as client:
        response = client.get(
            INDEX,
            timeout=10
        )
    logging.info(f"Response Content: {response.content}")
    assert response.status_code == 200
    assert response.json() == {"status": "Success"} # This is the basic response code set up already

def test_webhood():
    with httpx.Client(verify=False) as client:
        response = client.get(
            WEBHOOK_ENDPOINT,
            timeout=30
        )
    logging.info(f"Response Content: {response.content}")
    assert response.status_code == 200
