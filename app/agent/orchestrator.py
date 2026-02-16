from app.models import ProjectInput
from app.logger import get_logger
from app.agent.reasoning import ReasoningEngine # Renamed as Planning Agent
from app.agent.tools import RiskTooling          # Renamed as Technical Analyst
from app.agent.reflection import ReflectionEngine # Renamed as Reviewer Agent
from app.agent.evaluator import Evaluator        # Renamed as Quality Assurance Agent

class RiskAgent:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        # Initialize the Team of Specialized Agents
        self.planner = ReasoningEngine()       # Strategy & Pattern Matcher
        self.analyst = RiskTooling()           # Technical Risk Architect
        self.reviewer = ReflectionEngine()     # Critical Self-Reflector
        self.qa_lead = Evaluator()             # Final Quality Scorer

    def run(self, project: ProjectInput, context: str) -> dict:
        self.logger.info("Initializing Multi-Agent Collaborative Workflow")

        # 1. Planning Agent: Analyzes RAG context and sets the strategy
        print("[Agent] Planning Agent: Analyzing historical patterns...")
        reasoning = self.planner.generate_plan(project, context)

        # 2. Analyst Agent: Uses technical tools to generate structured risks
        print("[Agent] Technical Analyst: Designing risk matrix and mitigations...")
        risks = self.analyst.generate_risks(project.model_dump_json(), context)
        mitigation = self.analyst.mitigation_plan(risks, project.model_dump_json())

        # 3. Reviewer Agent: Performs autonomous self-correction
        print("[Agent] Reviewer Agent: Critiquing plan for bias or generic advice...")
        reflection = self.reviewer.reflect()

        # 4. QA Lead: Evaluates the final output against project success metrics
        print("[Agent] QA Lead: Calculating final delivery confidence score...")
        evaluation = self.qa_lead.evaluate()

        return {
            "reasoning": reasoning,
            "risks": risks,
            "mitigation": mitigation,
            "reflection": reflection,
            "evaluation": evaluation
        }