from openai import OpenAI
from src.utils.config import settings

client = OpenAI(api_key=settings.OPEN_AI_KEY)

def classify_the_comment(input_message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": """You are an AI trained to analyze Instagram comments for purchasing intent. 
                            A comment indicates intent if it includes words or phrases related to buying, pricing, availability, 
                            orders, or requests for more details. Respond strictly with 'yes' if the comment suggests interest in 
                            purchasing; otherwise, respond with 'no'."""
            },
            {
                "role": "user", 
                "content": f"""Analyze the following Instagram comment and determine if the user expresses 
                            intent or interest in buying the product.
                            Comment: "{input_message}"
                            Response (yes/no):"""}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content
import openai