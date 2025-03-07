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

        Deliver the breakdown in the following well-structured markdown format according to below template:

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

        ## Estimated Time: Provide a precise estimate of the time required to complete this task in fixed hours, using whole numbers only (e.g., 8, 10, 12). If the estimated time is 8 hours or less, treat it as a single task. If the estimated time exceeds 8 hours but is still manageable within 1-2 days, provide a well-defined breakdown into smaller user stories. If the task requires more than 2 days, ensure it is divided into multiple detailed and independent stories, each adhering strictly to the INVEST principles, without any additional notes or further breakdown.
        """
        prompts.append((role, prompt))
    return prompts