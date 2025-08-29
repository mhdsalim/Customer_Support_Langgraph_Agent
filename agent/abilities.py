# 🛠️ agent/abilities.py (FULL, with all stages covered)

from langchain_core.tools import tool

# ---- Mock MCP clients (simulate COMMON vs ATLAS servers) ----
def mcp_common_client(ability_name: str, **kwargs):
    """Simulates a call to the COMMON server for internal abilities."""
    print(f"  📞 Calling COMMON Server for ability: '{ability_name}'")
    if ability_name == "solution_evaluation":
        return {"score": 85} # Example score < 90 to test escalation [cite: 103]
    if ability_name == "response_generation":
        return "Your issue will be resolved soon"
    return {"status": "success", "source": "COMMON"}

def mcp_atlas_client(ability_name: str, **kwargs):
    print(f"  📞 Calling ATLAS Server for ability: '{ability_name}'")
    if ability_name =='extract_answer' or ability_name== 'knowledge_base_search':

        return {"status": "success", "source": "ATLAS",'data':'data','key':'key','value':'value'}
    return {"status": "success", "source": "ATLAS"}


# =========================
#        ABILITIES
# =========================

# -------- Stage 1: INTAKE --------
@tool
def accept_payload(payload: dict) -> dict:
    """Capture incoming request payload (customer_name, email, query, priority, ticket_id)."""
    print("✅ Payload accepted into workflow.")
    return {"payload": payload}


# -------- Stage 2: UNDERSTAND --------
@tool
def parse_request_text(query: str) -> dict:
    """Convert unstructured request to structured data (COMMON)."""
    return mcp_common_client("parse_request_text", query=query)

@tool
def extract_entities(text: str) -> dict:
    """Identify product, account, dates (ATLAS)."""
    return mcp_atlas_client("extract_entities", text=text)


# -------- Stage 3: PREPARE --------
@tool
def normalize_fields(ticket_id: str) -> dict:
    """Standardize dates, codes, IDs (COMMON)."""
    return mcp_common_client("normalize_fields", ticket_id=ticket_id)

@tool
def enrich_records(ticket_id: str) -> dict:
    """Add SLA, historical ticket info (ATLAS)."""
    return mcp_atlas_client("enrich_records", ticket_id=ticket_id)

@tool
def add_flags_calculations(priority: str) -> dict:
    """Compute priority or SLA risk (COMMON)."""
    return mcp_common_client("add_flags_calculations", priority=priority)


# -------- Stage 4: ASK --------
@tool
def clarify_question(ticket_id: str, missing_field: list[str]) -> dict:
    """Request missing information from user (ATLAS)."""
    return mcp_atlas_client("clarify_question", ticket_id=ticket_id, missing_field=missing_field)


# -------- Stage 5: WAIT --------
@tool
def extract_answer(clarification: str) -> dict:
    """Capture concise response from user (ATLAS)."""
    return mcp_atlas_client("extract_answer", clarification=clarification)

@tool
def store_answer(payload: dict, clarification_answer: dict) -> dict:
    """Update payload with captured response (STATE management)."""
    payload[clarification_answer['key']] = clarification_answer['value']
    print(f"✅ Stored answer: {clarification_answer['key']}={clarification_answer['value']}")
    return {"payload": payload}


# -------- Stage 6: RETRIEVE --------
@tool
def knowledge_base_search(query: str) -> dict:
    """Lookup KB or FAQ (ATLAS)."""
    return mcp_atlas_client("knowledge_base_search", query=query)

@tool
def store_data(payload: dict, data : dict) -> dict:
    """Attach retrieved info to payload (STATE management)."""
    payload[data['key']] = data['value']
    print(f"✅ Stored data: {data['key']}={data['value']}")
    return {"payload": payload}


# -------- Stage 7: DECIDE --------
@tool
def solution_evaluation(context: str) -> dict:
    """Score potential solutions 1-100 (COMMON)."""
    return mcp_common_client("solution_evaluation", context=context)

@tool
def escalation_decision(ticket_id: str, reason: str) -> dict:
    """Assign to human agent if score <90 (ATLAS)."""
    return mcp_atlas_client("escalation_decision", ticket_id=ticket_id, reason=reason)

@tool
def update_payload(payload: dict, decision: str) -> dict:
    """Record decision outcomes (STATE management)."""
    payload['decision'] = decision
    print(f"✅ Updated payload with: {decision}")
    return {"payload": payload}


# -------- Stage 8: UPDATE --------
@tool
def update_ticket(ticket_id: str, status: str) -> dict:
    """Modify status, fields, priority (ATLAS)."""
    return mcp_atlas_client("update_ticket", ticket_id=ticket_id, status=status)

@tool
def close_ticket(ticket_id: str) -> dict:
    """Mark issue resolved (ATLAS)."""
    return mcp_atlas_client("close_ticket", ticket_id=ticket_id)


# -------- Stage 9: CREATE --------
@tool
def response_generation(prompt: str) -> str:
    """Draft customer reply (COMMON)."""
    return mcp_common_client("response_generation", prompt=prompt)


# -------- Stage 10: DO --------
@tool
def execute_api_calls(ticket_id: str) -> dict:
    """Trigger CRM/order system actions (ATLAS)."""
    return mcp_atlas_client("execute_api_calls", ticket_id=ticket_id)

@tool
def trigger_notifications(email: str, message: str) -> dict:
    """Notify customer (ATLAS)."""
    return mcp_atlas_client("trigger_notifications", email=email, message=message)


# -------- Stage 11: COMPLETE --------
@tool
def output_payload(payload: dict) -> dict:
    """Print final structured payload at end of workflow."""
    print("🎉 Final Payload:", payload)
    return {"payload": payload}


# ---- Export all tools for workflow loading ----
all_tools = [
    accept_payload,
    parse_request_text, extract_entities,
    normalize_fields, enrich_records, add_flags_calculations,
    clarify_question,
    extract_answer, store_answer,
    knowledge_base_search, store_data,
    solution_evaluation, escalation_decision, update_payload,
    update_ticket, close_ticket,
    response_generation,
    execute_api_calls, trigger_notifications,
    output_payload,
]
