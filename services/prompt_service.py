# Function to generate prompts for the relevant roles
def generate_prompts(task_description, relevant_roles):
    prompts = []
    for role in relevant_roles:
        prompt = f"""
        As a {role} agent, your responsibility is to break down the following task into meticulously crafted INVEST-style user stories.

        Task: "{task_description}"

        You must adhere strictly to the INVEST principles:
        - Independent
        - Negotiable
        - Valuable
        - Estimable
        - Small
        - Testable

        Deliver the breakdown in the following well-structured markdown format:

        ## Title  
        Provide a clear, concise, and well-defined user story title.

        ---------------

        ## Description
        Provide the clear description based on user story. (Example: As a developer, I want to implement SignalR connections secured by a token retrieved from the station’s `connect/token` endpoint, so that only authorized clients can establish real-time communication with the station.)

        **Details & Requirements**  
        1. Requirement Title (Example: **Token Acquisition**)  
           - Requirement description (Example: Clients call the `connect/token` endpoint to obtain a valid authentication token.)  
           - Requirement description (Example: Ensure tokens have appropriate scopes/claims for SignalR connections.)  

        2. Requirement Title (Example: **SignalR Connection**)  
           - Requirement description (Example: Include the acquired token in the connection headers (e.g., `Authorization: Bearer <token>`) when initializing the SignalR client.)  
           - Requirement description (Example: On the server side, validate the token for each SignalR connection request.)  

        (Continue providing titles and descriptions like the above...)

        ---

        **Acceptance Criteria**  
        - Clear acceptance criterion (Example: Clients can retrieve a token from the station’s `connect/token` endpoint.)  
        - Clear acceptance criterion (Example: Token-based authorization is enforced on every new SignalR connection attempt.)  

        (Continue adding more clear acceptance criteria as needed...)

        ---

        **Implementation Notes / Tasks**  
        - Provide a thorough description (Example: **API Setup**: Confirm the `connect/token` endpoint exists and returns valid tokens with the necessary claims.)  
        - Provide a thorough description (Example: **SignalR Server**: Update the server-side configuration to parse and validate the bearer token on connection.)  

        (Add more titles and descriptions as necessary...)

        ------------

        ## Estimated Time: Precisely estimate the time needed to implement this task in hours. Do not break down the task further if the estimated time is <= 1 day. If the estimated time exceeds 1-2 days, you must break down the task into multiple detailed and well-defined stories without any notes, further description, Notes or Final Breakdown.
        """
        prompts.append((role, prompt))
    return prompts