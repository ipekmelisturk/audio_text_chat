from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
)

def chat_with_agent(transcription):
    """
    Generate a response using OpenAI's ChatCompletion API based on the transcription.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcription}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
