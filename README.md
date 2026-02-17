# 🤖 AI Delivery Risk Agent
The architecture of the AI Delivery Risk Agent is designed as a modular, Multi-Agent RAG (Retrieval-Augmented Generation) system. By decoupling the knowledge retrieval from the reasoning steps, the system provides high-accuracy project risk assessments grounded in historical data.
1. **The RAG Pipeline (Data Layer)**
      The system starts by building a searchable "memory" of past project outcomes.
           Knowledge Source: An Excel-based dataset containing historical project retrospectives.
           Embedding Engine: Text data is processed into 768-dimensional vectors using models/gemini-embedding-001.
           Vector Store: These vectors are stored in a FAISS (Facebook AI Similarity Search) index for high-speed local retrieval.
           Persistence: The system implements a local index check—if the vector database exists on disk, it loads instantly to save API quota.
2. **Multi-Agent Orchestration (Reasoning Layer)**
      Instead of a single large prompt, the logic is distributed across a team of specialized agents to ensure depth and clarity.
           Planning Agent (ReasoningEngine): Analyzes the project input against historical patterns identified by the RAG system.
           Technical Analyst (RiskTooling): A tool-equipped agent that translates patterns into a structured JSON risk matrix and specific mitigations.
           Reviewer Agent (ReflectionEngine): An autonomous agent that critiques the generated output for bias or generic "AI-speak," ensuring the results are actionable.
           QA Lead (Evaluator): Performs the final validation, scoring the delivery confidence based on the identified risks.
3. **Execution & Fault Tolerance (Resilience Layer)**
      Operating on a Free Tier API requires architectural guardrails to prevent system crashes.
           Sequential Chaining: Agents execute in a specific order, where the output of one serves as the context for the next.
           Request Pacing: The Orchestrator enforces a 15-second cooling period between agent hand-offs. This prevents exceeding the 5–15 RPM (Requests Per Minute) limits of the Gemini API.
           Automatic Retries: The LLM client is configured with max_retries=6 to handle intermittent network issues or transient API throttling.

📂 Project Structure
Plaintext
ai-project-risk-agent/
├── app/
│   ├── agent/        # Agent logic (Planner, Analyst, Reviewer, QA)
│   ├── llm/          # LLM client & configuration
│   ├── rag/          # Vector store & RAG logic
│   └── config.py     # Environment settings
├── data/             # Knowledge base (retrospectives.xlsx)
├── main.py           # Entry point
└── .env              # (Not committed) API credentials

## 🛠️ Technology Stack
| Component | Technology |
| :--- | :--- |
| **Orchestration** | LangChain |
| **Language Model** | Google Gemini 1.5 Flash |
| **Data Processing** | Pandas |
| **Vector Search** | FAISS |
| **Configuration** | Pydantic Settings |

## 🚀 Getting Started
Follow these steps to set up and run the AI Delivery Risk Agent on your local machine.

📋 **Prerequisites**
* **Python 3.10+**
* **API Key**: Generate a key from [Google AI Studio]
**Configure Environment**: Create a `.env` file in the root folder:(GOOGLE_API_KEY=*****).

🏃 **Running the Application**
Once the environment is configured, execute the main script to start the risk analysis:
python main.py

🔍 **Usage Notes**
Input: The agent will prompt you for project details (name, type, timeline, etc.).
RAG Flow: On the first run, the system will parse retrospectives.xlsx to build the local FAISS index.
Output: The agent will generate a structured risk report including technical analysis, mitigation plans, and a final confidence score.


