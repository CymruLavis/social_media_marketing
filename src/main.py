from fastapi import FastAPI
import logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the terminal
    ],
)
# logger = logging.getLogger("my_fastapi_app")

app = FastAPI()

@app.get('/')
def root():
    logging.info("We made it to the root")
    return {"status": "Success"}

@app.get('/comment')
def root():
    logging.info("We made it to the comment")
    return {"status": "Success"}