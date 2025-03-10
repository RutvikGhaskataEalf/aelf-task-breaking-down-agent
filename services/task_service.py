from services.deepseek_service import fetch_deepseek_response
from roles import roles

# Function to get the most relevant title and brief description
def get_relevant_title_and_description(task_description):
    prompt = f"""
    Analyze the following task description and generate the most suitable and clear title and a brief description.

    Task: "{task_description}"

    Provide an appropriate title and a concise, user-friendly description for the task.
    """
    response_data = fetch_deepseek_response(prompt)
    content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    lines = content.split("\n")
    title = lines[0].replace("**Title:**", "").strip()
    description = lines[2].replace("**Description:**", "").strip() if len(lines) > 1 else ""
    return title, description