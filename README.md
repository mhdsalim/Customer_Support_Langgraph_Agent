# 🤖 LangGraph Customer Support Agent

This project implements a **multi-stage customer support agent** using **LangGraph**. It models a complex support workflow as a graph, where each node represents a distinct stage in the process.

The agent is designed to handle tasks from initial data intake to final resolution, demonstrating:

* State management
* Deterministic & non-deterministic execution
* Integration with external services

---

## ✨ Features

* **Graph-Based Workflow** → Customer support flow modeled as a graph with **11 stages**.
* **State Persistence** → Maintains a state object across all stages so context is never lost.
* **Orchestration Logic** → Supports both **deterministic (sequential)** and **non-deterministic (AI-driven)** stages.
* **Service Integration** → Simulates routing abilities to different microservices (ATLAS for external data, COMMON for internal tasks) via mock MCP clients.
* **Structured Output** → Processes an initial query and generates a **JSON payload** as its final output.

---

## 📂 Project Structure

The project is organized to separate configuration, source code, and data for clarity and maintainability.

```bash
lang-graph-customer-agent/
├── .env                 # Stores environment variables (e.g., GOOGLE_API_KEY)
├── config.yaml          # Defines the agent's persona, stages, and workflow
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation (you are here!)
├── run_demo.py          # Main script to run the agent
│
├── data/
│   └── sample_query.json   # Sample input for the demo
│
├── agent/
│   ├── __init__.py
│   ├── state.py           # Defines the AgentState object
│   ├── abilities.py       # Mocks MCP clients and defines available tools
│   └── workflow.py        # Core LangGraph implementation
│
└── output/
    └── ...                # Final JSON outputs are saved here
```

---

## ⚙️ Getting Started

### ✅ Prerequisites

* Python **3.9+**
* Git

### 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone <your-repository-url>
   cd lang-graph-customer-agent
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   * Rename `.env.example` to `.env` (if available), or create a new `.env` file.
   * Add your Google Gemini API key:

     ```bash
     GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
     ```

---

## ▶️ How to Run

From the project root, run:

```bash
python run_demo.py
```

The script will:

1. Load the sample query from `data/sample_query.json`.
2. Run the agent through all **11 workflow stages**, printing progress to the console.
3. Save the final structured JSON output in the `output/` directory with a unique name.

---

## 🌐 Workflow Stages

The agent processes requests through **11 stages**:

1. **INTAKE** → Accepts the initial payload
2. **UNDERSTAND** → Parses the query and extracts entities
3. **PREPARE** → Normalizes and enriches the ticket data
4. **ASK** → (Optional) Determines if clarifying questions are needed
5. **WAIT** → (Optional) Waits for user response
6. **RETRIEVE** → Searches knowledge base for relevant info
7. **DECIDE** → Evaluates solutions / escalates to human agent (**non-deterministic**)
8. **UPDATE** → Updates ticket status in external system
9. **CREATE** → Generates final customer response
10. **DO** → Executes API calls & notifications
11. **COMPLETE** → Outputs final structured payload

---

## 📜 Configuration

The agent’s behavior is defined in **`config.yaml`**.

* Defines the agent’s **persona**
* Lists workflow **stages**
* Allows modifying the workflow without changing core code

---



