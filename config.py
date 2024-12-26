from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve secrets
CLIENT_ID = os.getenv("CLIENT_ID")
SCOPES = os.getenv('SCOPES', '').split(',')
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0/me/messages'
TENANT = 'consumers'

# llms
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_EMAIl_BODY_CHARACTERS = 256