import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_endpoint = os.getenv("DEEPSEEK_ENDPOINT")
github_token = os.getenv("GITHUB_TOKEN")
repo_owner = os.getenv("REPO_OWNER")
repo_name = os.getenv("REPO_NAME")
project_id = os.getenv("PROJECT_ID")