from app.llm.gemini_client import get_llm
from app.models import ProjectInput

class ReasoningEngine:
    def __init__(self):
        # This now returns a ChatGoogleGenerativeAI instance via LangChain
        self.llm = get_llm()

    def generate_plan(self, project: ProjectInput, context: str) -> str:
        prompt = f"""
        You are a Senior AI Delivery Risk Analyst. 

        CRITICAL INSTRUCTION: Your analysis MUST be grounded in the provided Historical Context. 
        Look for patterns in the historical data that match this project's type or constraints.

        Current Project Details:
        {project.model_dump_json(indent=2)}

        Historical Context (Past Lessons Learned):
        {context}

        Generate your response in this order:
        1. HISTORICAL PATTERN MATCH: Identify if any risks from the Historical Context apply to this new project. Be specific.
        2. NEW POTENTIAL RISKS: Identify additional risks based on your general knowledge.
        3. STRUCTURED ACTION PLAN: Provide steps to prevent these specific historical failures from repeating.
        """
        ai_message = self.llm.invoke(prompt)
        return ai_message.content