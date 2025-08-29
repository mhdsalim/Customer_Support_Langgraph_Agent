# 📝 agent/state.py
from typing import TypedDict, List, Optional, Dict, Any

class AgentState(TypedDict):
    """
    Represents the state of the customer support workflow.
    It is passed between stages, accumulating data.
    """
    # Initial payload
    customer_name: str
    email: str
    query: str
    priority: str
    ticket_id: str
    
    # Data added during workflow
    structured_query: Optional[dict]
    entities: Optional[dict]
    enrichment_data: Optional[dict]
    sla_risk: Optional[str]
    clarification: Optional[str]             # Stage 4 ASK
    clarification_answer: Optional[dict]      # Stage 5 WAIT
    retrieved_data: Optional[dict]      # Stage 6 RETRIEVE
    solution_score: Optional[int]            # Stage 7 DECIDE
    escalated: bool                          # Stage 7 DECIDE
    decision: Optional[str]                  # Stage 7 DECIDE (human/auto)
    final_response: Optional[str]            # Stage 9 CREATE
    
    # Log of actions taken
    execution_log: List[str]
