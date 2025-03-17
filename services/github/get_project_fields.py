import requests
from config import github_token, project_id

GITHUB_TOKEN = github_token
PROJECT_ID = project_id

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

get_project_fields_query = f"""
{{
  node(id: "{PROJECT_ID}") {{
    ... on ProjectV2 {{
      fields(first: 20) {{
        nodes {{
          ... on ProjectV2SingleSelectField {{
            id
            name
            dataType
          }}
          ... on ProjectV2Field {{
            id
            name
            dataType
          }}
        }}
      }}
    }}
  }}
}}
"""

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": get_project_fields_query},
    headers=headers
)

fields_data = response.json()

for field in fields_data["data"]["node"]["fields"]["nodes"]:
    print(f"Field Name: {field['name']}, Field ID: {field['id']}, Data Type: {field['dataType']}")

