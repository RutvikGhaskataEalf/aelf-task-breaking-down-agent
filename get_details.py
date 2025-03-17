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
      fields(first: 50) {{
        nodes {{
          ... on ProjectV2SingleSelectField {{
            id
            name
            dataType
            options {{
              id
              name
            }}
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
print("fields_data", fields_data)

# Check if 'Type' field exists
type_field = next((field for field in fields_data['data']['node']['fields']['nodes'] if field['name'] == 'Type'), None)
print("Type field:", type_field)
