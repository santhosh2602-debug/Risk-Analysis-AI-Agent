import json
import time
from app.llm.gemini_client import get_llm
from app.models import Risk
from google.api_core import exceptions

class RiskTooling:
    def __init__(self):
        self.llm = get_llm()

    def generate_risks(self, project_data: str, context: str) -> list[Risk]:
        prompt = f"""
        Analyze the following project using the provided Historical Context.
        Project: {project_data}
        Historical Context: {context}

        TASK: Identify delivery risks. If a risk is mentioned in the Context, you MUST include it.
        Return as a JSON array ONLY. Fields: "name", "severity", "likelihood".
        """
        
        # Protective wait to avoid 429 during the multi-agent chain
        time.sleep(2) 
        
        ai_message = self.llm.invoke(prompt)
        content = ai_message.content
        
        if isinstance(content, list):
            content = " ".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in content])
        
        clean_content = content.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(clean_content)
            return [Risk(**item) for item in data]
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error parsing JSON: {e}")
            return []

    def mitigation_plan(self, risks: list[Risk], project_data: str) -> str:
        risks_summary = "\n".join([f"- {r.name} (Severity: {r.severity})" for r in risks])

        # Persona change: Strategic & Brief instead of "Expert Consultant"
        prompt = f"""
        You are the Execution Lead Agent. 
        TASK: Create a CONCISE mitigation plan for these risks.
        
        STRICT RULES:
        1. No introductions ("As an expert...").
        2. No summaries at the end.
        3. For each risk, provide exactly TWO bullet points:
           - Immediate Action
           - Long-term Guardrail
        4. Maximum 2 sentences per bullet point.

        Project: {project_data}
        Risks:
        {risks_summary}
        """

        # FAULT TOLERANCE: Retry loop for the 429 Error
        for attempt in range(3):
            try:
                # Add a mandatory gap before this call to reset the API burst limit
                time.sleep(15) 
                ai_message = self.llm.invoke(prompt)
                return ai_message.content
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"  [Rate Limit] Mitigation Agent is waiting for quota (Attempt {attempt+1}/3)...")
                    time.sleep(20) # Wait longer if we hit the limit
                else:
                    raise e
        
        return "Mitigation plan unavailable due to API rate limits. Please retry in 60 seconds."