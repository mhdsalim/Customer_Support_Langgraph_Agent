# ▶️ run_demo.py
import json
from pprint import pprint
from agent.workflow import app
from pathlib import Path
from datetime import datetime

def run_agent():
    """
    Runs the Lang Graph agent and saves the final state to a unique JSON file.
    """
    # Build a path to the data file relative to THIS script's location
    script_location = Path(__file__).resolve().parent
    file_path = script_location / "data" / "sample_query.json"

    # 1. Load sample customer query
    with open(file_path, 'r') as f:
        sample_input = json.load(f)

    # 2. Initialize the state for the graph
    initial_state = {
        "customer_name": sample_input["customer_name"],
        "email": sample_input["email"],
        "query": sample_input["query"],
        "priority": sample_input["priority"],
        "ticket_id": sample_input["ticket_id"],
        "execution_log": [],
        "escalated": False
    }

    print("🚀 Starting Customer Support Agent Workflow...")
    print("==============================================")
    
    # 3. Invoke the graph
    final_state = app.invoke(initial_state)

    print("\n==============================================")
    print("✅ Workflow Complete. Final State:")
    print("==============================================")
    
    # 4. Print the final structured payload
    pprint(final_state)

    # --- NEW SECTION: SAVE OUTPUT TO JSON FILE ---
    # Create an 'output' directory if it doesn't exist
    output_dir = script_location / "output"
    output_dir.mkdir(exist_ok=True)

    # Generate a unique filename using a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ticket_id = final_state.get("ticket_id", "unknown_ticket")
    output_filename = f"{ticket_id}_{timestamp}.json"
    output_path = output_dir / output_filename

    # Write the final state to the new JSON file
    with open(output_path, 'w') as f:
        json.dump(final_state, f, indent=4)
    
    print("\n==============================================")
    print(f"💾 Output successfully saved to: {output_path}")
    print("==============================================")
    # --- END NEW SECTION ---

if __name__ == "__main__":
    run_agent()