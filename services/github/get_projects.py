import requests
from config import github_token, project_id

GITHUB_TOKEN = github_token
PROJECT_ID = project_id

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

query = f"""
{{
  organization(login: "{OWNER}") {{
    projectsV2(first: 10) {{
      nodes {{
        id
        title
      }}
    }}
  }}
}}
"""

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

data = response.json()
print(data)
