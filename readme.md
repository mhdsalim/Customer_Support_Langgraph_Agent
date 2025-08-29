🤖 LangGraph Customer Support Agent
This project implements a multi-stage customer support agent using LangGraph. It models a complex support workflow as a graph, where each node represents a distinct stage in the process. The agent is designed to handle tasks from initial data intake to final resolution, demonstrating state management, deterministic and non-deterministic execution, and integration with external services.

✨ Features

Graph-Based Workflow: The entire customer support flow is modeled as a graph with 11 distinct stages. 


State Persistence: The agent maintains and passes a state object across all stages, ensuring context is never lost. 


Orchestration Logic: Supports both deterministic (sequential) and non-deterministic (dynamic, AI-driven) stages. 



Service Integration: Simulates routing abilities to different microservices (ATLAS for external data, COMMON for internal tasks) via mock MCP clients. 



Structured Output: The agent processes an initial query and generates a structured JSON payload as its final output. 

📂 Project Structure
The project is organized to separate configuration, source code, and data for clarity and maintainability.

lang-graph-customer-agent/
│
├── .env                  # Stores the GOOGLE_API_KEY
├── config.yaml           # Defines the agent's stages and persona
├── requirements.txt      # Project dependencies
├── README.md             # You are here!
├── run_demo.py           # Main script to run the agent
│
├── data/
│   └── sample_query.json # Sample input for the demo
│
├── agent/
│   ├── __init__.py
│   ├── state.py          # Defines the AgentState object
│   ├── abilities.py      # Mocks MCP clients and defines all tools
│   └── workflow.py       # Core LangGraph implementation
│
└── output/
    └── ...               # Final JSON outputs are saved here
⚙️ Getting Started
Follow these instructions to set up and run the project locally.

### Prerequisites
Python 3.9+

Git

### Installation
Clone the repository:

Bash

git clone <your-repository-url>
cd lang-graph-customer-agent
Create a virtual environment:

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
Install dependencies:

Bash

pip install -r requirements.txt
Set up your API Key:

Rename the .env.example file to .env (if you have one) or create a new file named .env.

Open the .env file and add your Google Gemini API key:

GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
▶️ How to Run
Execute the main demo script from the root directory of the project.

Bash

python run_demo.py
The script will:

Load the sample query from data/sample_query.json.

Run the agent through all 11 workflow stages, printing progress to the console.

Save a uniquely named JSON file with the complete final state in the output/ directory.

🌐 Workflow Stages
The agent processes requests by moving through the following 11 stages in sequence: 


INTAKE: Accepts the initial payload. 


UNDERSTAND: Parses the query and extracts entities. 


PREPARE: Normalizes and enriches the ticket data. 


ASK: (Optional) Determines if clarifying questions are needed. 


WAIT: (Optional) Waits for a user's response. 


RETRIEVE: Searches a knowledge base for relevant information. 


DECIDE: Evaluates solutions and makes decisions, such as escalating to a human agent (this is the non-deterministic stage). 


UPDATE: Updates the ticket status in an external system. 



CREATE: Generates the final response for the customer. 



DO: Executes final API calls and triggers notifications. 


COMPLETE: Outputs the final structured payload. 

📜 Configuration
The agent's behavior is defined in config.yaml. This file specifies the agent's persona and lists the stages of the workflow. This allows for easy modification of the agent's structure without changing the core code.