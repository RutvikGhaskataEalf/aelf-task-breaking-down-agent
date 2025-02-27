import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import re

# Load environment variables
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_endpoint = os.getenv("DEEPSEEK_ENDPOINT")

# Flask app setup
app = Flask(__name__)

# Agent roles
roles = [
    "Backend Developer",
    "Frontend Developer",
    "UI/UX Designer",
    "Product Manager"
]

# Function to determine relevant roles using Deepseek AI
def get_relevant_roles(task_description):
    analysis_prompt = f"""
    Carefully analyze the following task description and determine the most suitable roles from the list below. 
    Only select roles directly responsible for implementing the specific technical or strategic requirements of the task.

    Roles: {', '.join(roles)}

    Task: "{task_description}"

    Consider the expertise required and the scope of the task. Respond only with the most relevant roles.
    """
    headers = {
        "Content-Type": "application/json",
        "api-key": deepseek_api_key
    }

    payload = {
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": analysis_prompt}],
        "temperature": 0.7,
        "stream": False
    }

    response = requests.post(f"{deepseek_endpoint}/chat/completions?api-version=2024-02-15-preview",
                             headers=headers,
                             json=payload)
    response_data = response.json()
    identified_roles = [role for role in roles if role in response_data.get("choices", [{}])[0].get("message", {}).get("content", "")]
    return identified_roles if identified_roles else roles


# Function to generate prompts for the relevant roles
def generate_prompts(task_description, relevant_roles):
    prompts = []
    for role in relevant_roles:
        prompt = f"""
        As a {role} agent, break down the following task into INVEST-style user stories. 

        Task: "{task_description}"

        Follow the INVEST principles:
        - Independent
        - Negotiable
        - Valuable
        - Estimable
        - Small
        - Testable

        Provide the breakdown in the following markdown format:

        **User Story**  
        Describe the user story clearly. (example like this : As a developer, I want to implement SignalR connections secured by a token retrieved from the station’s `connect/token` endpoint, so that only authorized clients can establish real-time communication with the station.)

        ---

        **Details & Requirements**  
        1. Requirement Title (example like this: **Token Acquisition** )
           - requirement description (example like this: Clients call the `connect/token` endpoint to obtain a valid authentication token.)
           - requirement description (example ike this: Ensure tokens have appropriate scopes/claims for SignalR connections. )

        2. Requirement Title (example like this: **SignalR Connection** )
           - requirement description (example like this: Include the acquired token in the connection headers (e.g., `Authorization: Bearer <token>`) when initializing the SignalR client.)
           - requirement description (example like this: On the server side, validate the token for each SignalR connection request.  )

        (more title/description like above...)


        ---

        **Acceptance Criteria**  
        - Clear acceptance criterion (example like this: - Clients can retrieve a token from the station’s `connect/token` endpoint.)
        - Clear acceptance criterion (example like this: - Token-based authorization is enforced on every new SignalR connection attempt.)

        (more Clear acceptance criterion like above...)

        ---

        **Implementation Notes / Tasks**  
        - [Title] : describle in description (example like this: - **API Setup**: Confirm the `connect/token` endpoint exists and returns valid tokens with the necessary claims.  )
        - [Title] : describle in description (example like this: - **SignalR Server**: Update the server-side configuration to parse and validate the bearer token on connection. )

        (more title/description like above...)

        **Estimated Time:** Provide the estimated time to implement this task.
        Do not break down the task further if estimated time <= 1 day and estimate time in hours

        =======================================================================

        Note: That you need to make sure

        - If estimate time if more than 1-2 days then please breakdown a task in multiple stories. 
        """
        prompts.append((role, prompt))
    return prompts

# Function to call Deepseek API for task breakdown and structure the output
def call_deepseek_api(prompts):
    results = {"stories": {}}
    for role, prompt in prompts:
        headers = {
            "Content-Type": "application/json",
            "api-key": deepseek_api_key
        }

        payload = {
            "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            "temperature": 0.7,
            "stream": False
        }

        response = requests.post(f"{deepseek_endpoint}/chat/completions?api-version=2024-02-15-preview",
                                 headers=headers,
                                 json=payload)
        response_data = response.json()
        story_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

        results["stories"][role] = story_content
    return results

# API endpoint to break down tasks
@app.route("/api/ai-agent/invest-task", methods=["POST"])
def invest_task():
    data = request.json
    task_description = data.get("task_description")
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    relevant_roles = get_relevant_roles(task_description)
    print("relevant_roles",relevant_roles)
    prompts = generate_prompts(task_description, relevant_roles)
    responses = call_deepseek_api(prompts)
    return jsonify(responses)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
