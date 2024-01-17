"""
This module contains templates specific for the usage of LLM advisory tasks. For this tasks it is nessacary to define which tasks the LLM has to do, since the prompt
is taks dependent, given the context from the retriever. Hence templates define specific tasks, which the LLM has to do. Therefore earch class represents a tasks.

In the case of Legal advisory tasks, templates can be created wrt the following tasks in Legal advisory tasks:

- Preparing for Depositions (https://www.legalpromptguide.com/2.-practical-prompt-engineering-strategies-and-techniques/2.2.-few-example-prompting#example-preparing-for-depositions)
- ...
"""

class Legal_Template:
    def __init__(self):
        super().__init__()
        self.task_Depositions_Template = "Prepare questions for depositions."
        self.agents_profession = "Legal professional"
        self.sign_off = "Thank you for using our service."

    def task1_template(self):
        # Concrete implementation of the method
        template = """
            Generate information based only on the following context: {context}
            
            Prompt: As a {self.agents_profession} {self.task_Depositions_Template}

            Examples:
            Input: Generate questions to ask a witness during a deposition in a car accident case?
            Output:
            - Can you describe the events leading up to the accident?
            - What were the weather and road conditions?
            - Did you admit fault or make any statements about the accident at the scene?

            Input: Create a list of questions to ask a defendant during a deposition in a 
            workplace discrimination case?
            Output:
            - Are you aware of the company's policies regarding workplace discrimination?
            - Did the plaintiff make you aware of the alleged discriminatory behavior? 
            - Were any actions taken by the company after the alleged incidents were reported?

            Input: {Questions}
            Output:
        """
        return template
