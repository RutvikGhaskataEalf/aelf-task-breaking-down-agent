# Function to generate prompts for the relevant roles
def generate_prompts(task_description, relevant_roles):
    prompts = []
    for role in relevant_roles:
        prompt = f"""
        As a {role} agent, your responsibility is to break down the following task into meticulously crafted INVEST-style user stories which should be align with your role.

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
        A well-defined user story in this format: "As a [role], I want [objective] so that [benefit]."

        **Details & Requirements**  
        1. **Requirement Title**  
           - Specific and detailed requirement description.  
           - Additional key requirement or condition.  

        2. **Requirement Title**  
           - Specific and detailed requirement description.  
           - Additional key requirement or condition.  

        (Continue listing requirements as needed...)

        -----------------

        **Acceptance Criteria**  
        - Clear, measurable acceptance criterion ensuring story completion.  
        - Additional acceptance criterion as needed. 

        (Add more acceptance criteria for comprehensive validation...)

        -----------------

        **Implementation Notes / Tasks**  
        - **Task Title**: Detailed explanation of the task.  
        - **Task Title**: Detailed explanation of the task. 

        (Break down into granular, actionable tasks...)

        ------------

        ## Estimated Time: Provide a well-reasoned, fixed-hour estimate (e.g., 4, 8, 12). If the estimate exceeds 8 hours but remains within 1-2 days, break it down into smaller, well-defined stories. If the task requires more than 2 days, decompose it into multiple independent stories strictly aligned with the INVEST principles.
        """
        prompts.append((role, prompt))
    return prompts