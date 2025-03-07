from flask import Flask, request, jsonify
from services.role_service import get_relevant_roles
from services.prompt_service import generate_prompts
from services.deepseek_service import fetch_deepseek_response
from services.parse_response import parse_text
    
# Flask app setup
app = Flask(__name__)

# API endpoint to break down tasks
@app.route("/api/ai-agent/invest-task", methods=["POST"])
def invest_task():
    data = request.json
    task_description = data.get("task_description")
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    relevant_roles = get_relevant_roles(task_description)
    prompts = generate_prompts(task_description, relevant_roles)

    results = {"stories": {}}
    for role, prompt in prompts:
        response_data = fetch_deepseek_response(prompt)
        story_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print("story_content",story_content)
        formatedResponse = parse_text(story_content)
        results["stories"][role] = formatedResponse

    return jsonify(results)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
