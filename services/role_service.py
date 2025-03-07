from services.deepseek_service import fetch_deepseek_response
from roles import roles

# Function to determine relevant roles using Deepseek AI
def get_relevant_roles(task_description):
    analysis_prompt = f"""
    Analyze the following task description and identify only the most essential and highly relevant roles from the list below.

    Roles: {', '.join(roles)}

    Task: "{task_description}"

    Select exclusively the roles crucial for the successful and complete implementation of the task requirements.
    """
    response_data = fetch_deepseek_response(analysis_prompt)
    identified_roles = [role for role in roles if role in response_data.get("choices", [{}])[0].get("message", {}).get("content", "")]
    return identified_roles if identified_roles else roles