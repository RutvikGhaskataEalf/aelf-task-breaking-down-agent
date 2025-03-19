# AI Agents for breaking down a sentence into INVEST-style user stories

## Project Structure

```
project-root/
|-- app.py                  # Main Flask app
|-- config.py               # Environment setup and config variables
|-- roles.py                # Predefined agent roles
|-- services/
|   |-- deepseek_service.py # Deepseek API interactions
|   |-- role_service.py     # Role identification logic
|   |-- prompt_service.py   # Prompt generation logic
```

## Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

- Activate it:

   - On Windows:
    ```bash
     venv\Scripts\activate
    ```

   - On Mac/Linux:
    ```bash
     source venv/bin/activate
    ```

## Install required packages

```bash
pip install requests python-dotenv flask flask-cors
```

## Set up environment variables
You’ve already got a `.env` file. Ensure it’s in the root of your project and has:

```bash
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_ENDPOINT=https://your-endpoint-here
```

## Run app

```bash
python app.py
```

API should start on `http://127.0.0.1:5000`.

## Test the API endpoint
You can send a POST request to the API endpoint like this:

```bash
curl -X POST http://127.0.0.1:5000/api/ai-agent/invest-task \
-H "Content-Type: application/json" \
-d '{"repo_owner": "XXXXXXXXXXX","repo_name": "hello-world","project_id": "XXXXXXXXXXX","task_description": "Build a new feature for the app","estimate_field_id": "XXXXXXXXXXX"}'
```