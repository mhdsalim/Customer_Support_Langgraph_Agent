# 🌐 agent/workflow.py
from langgraph.graph import StateGraph, END
from .state import AgentState
from . import abilities

# --- STAGE (NODE) DEFINITIONS ---

def execute_intake(state: AgentState) -> AgentState:
    print("--- 1. STAGE: INTAKE ---")
    # Ability: accept_payload
    abilities.accept_payload.invoke({"payload": dict(state)})
    state['execution_log'].append("Payload accepted.")
    return state

def execute_understand(state: AgentState) -> AgentState:
    print("--- 2. STAGE: UNDERSTAND ---")
    # Abilities: parse_request_text, extract_entities
    state['structured_query'] = abilities.parse_request_text.invoke({"query": state['query']})
    state['entities'] = abilities.extract_entities.invoke({"text": state['query']})
    state['execution_log'].append("Query parsed and entities extracted.")
    return state

def execute_prepare(state: AgentState) -> AgentState:
    print("--- 3. STAGE: PREPARE ---")
    # Abilities: normalize_fields, enrich_records, add_flags_calculations
    abilities.normalize_fields.invoke({"ticket_id": state['ticket_id']})
    state['enrichment_data'] = abilities.enrich_records.invoke({"ticket_id": state['ticket_id']})
    state['sla_risk'] = abilities.add_flags_calculations.invoke({"priority": state['priority']})
    state['execution_log'].append("Data normalized, enriched, and flags calculated.")
    return state
    
def execute_ask(state: AgentState) -> AgentState:
    print("--- 4. STAGE: ASK ---")
    
    # Check for missing important fields
    missing_fields = []
    if not state.get("customer_name"):
        missing_fields.append("customer_name")
    if not state.get("email"):
        missing_fields.append("email")
    if not state.get("query"):
        missing_fields.append("query")

    if missing_fields:
        # If missing fields → trigger clarify ability
        clarification_text = f"Missing fields: {', '.join(missing_fields)}. Please provide them."
        state['clarification'] = clarification_text
        abilities.clarify_question.invoke({"ticket_id":state['ticket_id'], "missing_field":missing_fields})
        state['execution_log'].append(f"Clarification requested for: {missing_fields}")
    else:
        # No missing info → skip
        state['clarification'] = None
        state['execution_log'].append("No clarification needed.")
    
    return state




def execute_wait(state: AgentState) -> AgentState:
    print("--- 5. STAGE: WAIT ---")
    
    if state.get("clarification"):
        # Simulate waiting for user response
        response = abilities.extract_answer.invoke({"clarification": state['clarification']})
        state['clarification_answer'] = {
            "data": response.get("data"),
            "key": response.get("key"),
            "value": response.get("value")
        }
        abilities.store_answer.invoke({
            "payload": state,
            "clarification_answer": state['clarification_answer']
            
        })
        state['execution_log'].append(f"User answered clarification: {state['clarification_answer']}")
    else:
        state['execution_log'].append("No clarification was needed, skipping WAIT.")
    
    return state


def execute_retrieve(state: AgentState) -> AgentState:
    print("--- 6. STAGE: RETRIEVE ---")
    # Abilities: knowledge_base_search, store_data
    knowledge_base_data= abilities.knowledge_base_search.invoke({"query": state['query']})
    state['retrieved_data'] = {
        "data": knowledge_base_data.get("data"),
        "key": knowledge_base_data.get("key"),
        "value": knowledge_base_data.get("value")
    }

    abilities.store_data.invoke({"payload": state, "data": state['retrieved_data']})
    state['execution_log'].append("Knowledge base searched and data stored.")
    return state

def execute_decide(state: AgentState) -> AgentState:
    print("--- 7. STAGE: DECIDE (Non-Deterministic) ---")
    # Abilities: solution_evaluation, escalation_decision, update_payload
    context = f"Retrieved data: {state['retrieved_data']}"
    eval_result = abilities.solution_evaluation.invoke({"context": context})
    score = eval_result.get("score", 100)
    state["solution_score"] = score
    
    if score < 90:
        abilities.escalation_decision.invoke({
            "ticket_id": state["ticket_id"],
            "reason": f"Solution score {score} is below threshold."
        })
        state["escalated"] = True
        decision = f"Escalate (Score: {score})"
    else:
        state["escalated"] = False
        decision = f"Auto-resolve (Score: {score})"
    
    abilities.update_payload.invoke({"payload": state, "decision": decision})
    state['execution_log'].append(f"Decision made: {decision}")
    return state
    
def execute_update(state: AgentState) -> AgentState:
    print("--- 8. STAGE: UPDATE ---")
    # Abilities: update_ticket, close_ticket
    if state["escalated"]:
        abilities.update_ticket.invoke({"ticket_id": state["ticket_id"], "status": "Escalated"})
        state['execution_log'].append("Ticket status updated to Escalated.")
    else:
        abilities.close_ticket.invoke({"ticket_id": state["ticket_id"]})
        state['execution_log'].append("Ticket closed.")
    return state

def execute_create(state: AgentState) -> AgentState:
    print("--- 9. STAGE: CREATE ---")
    # Ability: response_generation
    response_data = abilities.response_generation.invoke({
        "prompt": f"Draft a professional reply for: {state['query']}"
    })
    state['final_response'] = response_data
    state['execution_log'].append("Customer response generated.")
    return state

def execute_do(state: AgentState) -> AgentState:
    print("--- 10. STAGE: DO ---")
    # Abilities: execute_api_calls, trigger_notifications
    abilities.execute_api_calls.invoke({"ticket_id": state["ticket_id"]})
    abilities.trigger_notifications.invoke({
        "email": state["email"],
        "message": state['final_response']
    })
    state['execution_log'].append("Final API calls executed and notifications sent.")
    return state

def execute_complete(state: AgentState) -> AgentState:
    print("--- 11. STAGE: COMPLETE ---")
    # Ability: output_payload
    abilities.output_payload.invoke({"payload": dict(state)})
    state['execution_log'].append("Workflow finished and payload output.")
    return state

# --- GRAPH DEFINITION ---

workflow = StateGraph(AgentState)

# Add nodes for each stage
workflow.add_node("INTAKE", execute_intake)
workflow.add_node("UNDERSTAND", execute_understand)
workflow.add_node("PREPARE", execute_prepare)
workflow.add_node("ASK", execute_ask)
workflow.add_node("WAIT", execute_wait)
workflow.add_node("RETRIEVE", execute_retrieve)
workflow.add_node("DECIDE", execute_decide)
workflow.add_node("UPDATE", execute_update)
workflow.add_node("CREATE", execute_create)
workflow.add_node("DO", execute_do)
workflow.add_node("COMPLETE", execute_complete)

# Define the sequential edges for the workflow
workflow.set_entry_point("INTAKE")
workflow.add_edge("INTAKE", "UNDERSTAND")
workflow.add_edge("UNDERSTAND", "PREPARE")
workflow.add_edge("PREPARE", "ASK")
workflow.add_edge("ASK", "WAIT")
workflow.add_edge("WAIT", "RETRIEVE")
workflow.add_edge("RETRIEVE", "DECIDE")
workflow.add_edge("DECIDE", "UPDATE")
workflow.add_edge("UPDATE", "CREATE")
workflow.add_edge("CREATE", "DO")
workflow.add_edge("DO", "COMPLETE")
workflow.add_edge("COMPLETE", END)

# Compile the graph
app = workflow.compile()
