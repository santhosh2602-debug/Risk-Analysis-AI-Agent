from app.models import ProjectInput
from app.rag.retriever import ContextRetriever
from app.agent.orchestrator import RiskAgent
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from app.rag.vector_store import build_vector_store_from_excel

console = Console()

def get_project_from_user():
    console.print("[bold cyan]--- Enter Project Details for Risk Analysis ---[/bold cyan]")
    
    name = Prompt.ask("Project Name")
    p_type = Prompt.ask("Project Type", choices=["Fixed Price", "T&M", "Internal"], default="Fixed Price")
    timeline = IntPrompt.ask("Timeline (months)", default=6)
    size = IntPrompt.ask("Team Size", default=5)
    clarity = Prompt.ask("Requirements Clarity", choices=["Clear", "Partial", "Vague"], default="Partial")
    
    # Simple list input for dependencies
    deps_raw = Prompt.ask("Dependencies (comma separated)", default="None")
    deps = [d.strip() for d in deps_raw.split(",")]

    return ProjectInput(
        project_type=p_type,
        timeline_months=timeline,
        team_size=size,
        requirements_clarity=clarity,
        dependencies=deps
    )

project = get_project_from_user()

vector_store = build_vector_store_from_excel("data/retrospectives.xlsx")

retriever = ContextRetriever(vector_store)
agent = RiskAgent()

#project = ProjectInput(
#    project_type="Fixed Price",
#    timeline_months=4,
#    team_size=6,
#    requirements_clarity="Partial",
#    dependencies=["External Vendor"]
#)

context = retriever.retrieve(project.model_dump_json(indent=2), k=4)
result = agent.run(project, context)

#print(result)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


with console.status("[bold green]Agent is analyzing risks...") as status:
    # 1. Retrieval & Reasoning
    context = retriever.retrieve(project.model_dump_json(), k=4)
    result = agent.run(project, context) # Assuming result is a dict with 'risks' and 'mitigation'

# --- STRUCTURED OUTPUT SECTION ---

# 1. Display Project Summary Panel
console.print(Panel(f"[bold blue]Project Type:[/bold blue] {project.project_type}\n"
                    f"[bold blue]Timeline:[/bold blue] {project.timeline_months} months\n"
                    f"[bold blue]Team Size:[/bold blue] {project.team_size}", 
                    title="Project Input Summary", expand=False))

# 2. Display Risks in a Table
table = Table(title="Identified Delivery Risks", show_header=True, header_style="bold magenta")
table.add_column("Risk Name", style="dim", width=30)
table.add_column("Severity", justify="center")
table.add_column("Likelihood", justify="center")

for risk in result['risks']:
    # Color coding based on severity
    color = "red" if risk.severity == "High" else "yellow" if risk.severity == "Medium" else "green"
    table.add_row(risk.name, f"[{color}]{risk.severity}[/{color}]", risk.likelihood)

console.print(table)

# 3. Display Mitigation Plan in a Panel
mitigation_text = result['mitigation']
if isinstance(mitigation_text, list):
    mitigation_text = mitigation_text[0].get('text', str(mitigation_text))

console.print(Panel(mitigation_text, title="[bold green]AI Mitigation Strategy[/bold green]", border_style="green"))
