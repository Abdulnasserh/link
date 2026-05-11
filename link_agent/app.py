"""
link_agent — A2A application entry point.

Start the server with:
    uvicorn link_agent.app:a2a_app --host 0.0.0.0 --port 8001

The agent card is served publicly at:
    GET http://localhost:8001/.well-known/agent-card.json

All other endpoints require an X-API-Key header (see shared/middleware.py).
"""
import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="link_transition_care_agent",
    description=(
        "A Transition of Care Specialist that resolves the 'Post-Discharge Black Hole'. "
        "Monitors pending ghost labs, reconciles medications, and assesses clinical risks "
        "during the critical period after a patient leaves the hospital."
    ),
    url=os.getenv("LINK_AGENT_URL", os.getenv("BASE_URL", "http://localhost:8001")),
    port=8001,
    # This URI is the key under which callers send FHIR credentials in the
    # A2A message metadata.
    fhir_extension_uri=f"{os.getenv('PO_PLATFORM_BASE_URL', 'http://localhost:5139')}/schemas/a2a/v1/fhir-context",
    # SMART-on-FHIR scopes — one per FHIR resource type accessed by the tools.
    fhir_scopes=[
        {"name": "patient/Patient.rs",           "required": True},
        {"name": "patient/MedicationRequest.rs", "required": True},
        {"name": "patient/Condition.rs",         "required": True},
        {"name": "patient/Observation.rs",       "required": True},
        {"name": "patient/DiagnosticReport.rs",  "required": True},
    ],
    skills=[
        AgentSkill(
            id="post-discharge-assessment",
            name="post-discharge-assessment",
            description="Perform a comprehensive post-discharge risk assessment including ghost lab detection, medication reconciliation, and clinical handover report generation.",
            tags=["post-discharge", "ghost-labs", "handover", "fhir"],
        ),
        AgentSkill(
            id="ghost-lab-detection",
            name="ghost-lab-detection",
            description="Detect pending or preliminary lab results (ghost labs) that were ordered during hospitalization but not finalized before discharge.",
            tags=["ghost-labs", "diagnostics", "fhir"],
        ),
        AgentSkill(
            id="medication-reconciliation",
            name="medication-reconciliation",
            description="Reconcile active medications during care transitions and flag potential conflicts.",
            tags=["medications", "reconciliation", "fhir"],
        ),
        AgentSkill(
            id="clinical-risk-correlation",
            name="clinical-risk-correlation",
            description="Correlate active conditions with pending lab results and medications to assess post-discharge clinical risk level.",
            tags=["risk-assessment", "conditions", "fhir"],
        ),
    ],
)
