import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_endpoint = os.getenv("DEEPSEEK_ENDPOINT")