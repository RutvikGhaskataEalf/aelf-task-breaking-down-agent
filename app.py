from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import re
from services.role_service import get_relevant_roles
from services.task_service import get_relevant_title_and_description
from services.prompt_service import generate_prompts
from services.deepseek_service import fetch_deepseek_response
from services.parse_response import parse_text
from services.transform_input import transform_input

app = Flask(__name__)
CORS(app)

# {
#     "repo_owner": "XXXXXXXXXXX",
#     "repo_name": "hello-world",
#     "project_id": "XXXXXXXXXXX",
#     "task_description": "As a developer, I want to build a login page so that users can log in to the application."
#     "end_date_field_id": "XXXXXXXXXXX"
# }

@app.route("/api/ai-agent/invest-task", methods=["POST"])
def invest_task():
    data = request.json
    GITHUB_TOKEN = request.headers.get("Token")
    REPO_OWNER = data.get("repo_owner")
    REPO_NAME = data.get("repo_name")
    PROJECT_ID = data.get("project_id")

    print("GITHUB_TOKEN: ", GITHUB_TOKEN)
    print("REPO_OWNER: ", REPO_OWNER)
    print("REPO_NAME: ", REPO_NAME)
    print("PROJECT_ID: ", PROJECT_ID)

    if not GITHUB_TOKEN or not REPO_OWNER or not REPO_NAME or not PROJECT_ID:
        return jsonify({"error": "Missing required parameters"}), 400
        
    HEADERS = {
    'Authorization': f'bearer {GITHUB_TOKEN}',
    'Content-Type': 'application/json'
   }

    task_description = data.get("task_description")
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    relevant_roles = get_relevant_roles(task_description)
    prompts = generate_prompts(task_description, relevant_roles)

    results = {"stories": {}}
    for role, prompt in prompts:
        response_data = fetch_deepseek_response(prompt)

        story_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        formatedResponse = parse_text(story_content)
        results["stories"][role] = formatedResponse

    issues_data = transform_input(results)

    headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
    }

    # Get the relevant title and description
    main_title, main_description = get_relevant_title_and_description(task_description)

    # Create apic task 
    epic_issue_data = {
        'title': f"{main_title}",
        'body': f"{main_description}",
    }

    epic_issue_response = requests.post(
        f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues',
        headers=headers,
        json=epic_issue_data
    )

    epicIssueJson = epic_issue_response.json()
    
    print(f"Epic issue created: {epicIssueJson}")
    
    epic_issue_number = epicIssueJson["number"]
    
    # Create GitHub issues for each role
    issues_created = []
    for issue in issues_data:
        issue_data = {
            'title': f"{issue['Title']}",
            'body': f"**Description:** {issue['Description']}\n\n**Estimated Time:** {issue['Estimated Time']}",
            'labels': [issue['Role']]
        }

        issue_response = requests.post(
            f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues',
            headers=headers,
            json=issue_data
        )

        if issue_response.status_code == 201:
            issueJson = issue_response.json()
            
            issue_id = issueJson["id"]

            subissue_data = {
                'sub_issue_id': issue_id
            }
            # Add subtask
            subtask_response = requests.post(
                f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{epic_issue_number}/sub_issues',
                headers=headers,
                json=subissue_data
            )

            # Add the issue to the GitHub project using GraphQL
            graphql_query = {
                'query': f"""
                mutation {{
                    addProjectV2ItemById(input: {{
                        projectId: \"{PROJECT_ID}\",
                        contentId: \"{issueJson['node_id']}\"
                    }}) {{
                        item {{
                            id
                        }}
                    }}
                }}
                """
            }

            project_response = requests.post(
                'https://api.github.com/graphql',
                headers=HEADERS,
                json=graphql_query
            )

            add_item_data = project_response.json()
            item_id = add_item_data["data"]["addProjectV2ItemById"]["item"]["id"]
            print(f"Issue added to project with item ID: {item_id}")
            
            field_id = data.get("estimate_field_id") 

            print(f"Field ID: {field_id}")

            # Only update field if field_id is provided
            if field_id and item_id:
                try:
                    estimate_value = int(re.search(r'\d+', issue['Estimated Time']).group())
                    update_field_query = f"""
                    mutation {{
                      updateProjectV2ItemFieldValue(input: {{
                        projectId: "{PROJECT_ID}",
                        itemId: "{item_id}",
                        fieldId: "{field_id}",
                        value: {{
                           number: {float(estimate_value)}
                        }}
                      }}) {{
                        projectV2Item {{
                          id
                        }}
                      }}
                    }}
                    """
                    
                    response = requests.post(
                        "https://api.github.com/graphql",
                        json={"query": update_field_query},
                        headers=headers
                    )
                    
                    update_field_data = response.json()
                    print(f"Estimate time added to issue: {update_field_data}")
                except Exception as e:
                    print(f"Failed to update field: {str(e)}")

            if project_response.status_code == 200:
                issues_created.append({"title": issue_data['title'], "status": "success"})
            else:
                issues_created.append({"title": issue_data['title'], "status": "failed", "details": project_response.json()})
        else:
            issues_created.append({"title": issue_data['title'], "status": "failed", "details": issue_response.json()})

    return jsonify({'message': 'Issues creation process completed', 'issues': issues_created, "output": issues_data, "results": results}), 201

if __name__ == "__main__":
    app.run(debug=True)
