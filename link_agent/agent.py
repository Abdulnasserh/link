"""
link_agent — Agent definition.

This agent is a "Transition of Care Specialist" that resolves the
Post-Discharge Black Hole. It has read-only access to a patient's FHIR R4
record and specializes in:
  - Detecting pending "ghost labs" (DiagnosticReports not yet finalized)
  - Medication reconciliation during care transitions
  - Correlating active conditions with pending results for risk assessment

FHIR credentials (server URL, bearer token, patient ID) are injected via
A2A message metadata by the caller (e.g. Prompt Opinion) and extracted into
session state by extract_fhir_context before every LLM call.
"""
import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from shared.fhir_hook import extract_fhir_context
from shared.tools import (
    get_active_conditions,
    get_active_medications,
    get_patient_demographics,
    get_recent_observations,
)

# ── Model selection ────────────────────────────────────────────────────────────
# Set LINK_AGENT_MODEL in your .env to switch models.
# Default: gemini/gemini-2.5-flash via Google AI Studio
_model_name = os.getenv("LINK_AGENT_MODEL", "gemini/gemini-2.5-flash")
_model = LiteLlm(model=_model_name)

root_agent = Agent(
    name="link_transition_care_agent",
    model=_model,
    description=(
        "A Transition of Care Specialist that resolves the 'Post-Discharge Black Hole'. "
        "Monitors pending ghost labs, reconciles medications, and assesses clinical risks "
        "during the critical period after a patient leaves the hospital."
    ),
    instruction=(
        "You are Link, a Transition of Care Specialist with secure, read-only access to a patient's FHIR health record. "
        "Your mission is to prevent the 'Post-Discharge Black Hole' — the dangerous gap in care that occurs "
        "when patients leave the hospital before all lab results are finalized.\n\n"
        "When asked about a patient, follow this clinical workflow:\n"
        "1. First, retrieve the patient's demographics to confirm identity.\n"
        "2. Check for pending or preliminary diagnostic reports (ghost labs) using observations.\n"
        "3. Retrieve the active medication list for reconciliation.\n"
        "4. Review active conditions to correlate with pending results.\n"
        "5. Synthesize your findings into a structured Post-Discharge Handover Report.\n\n"
        "In your handover report, always include:\n"
        "- Patient identification\n"
        "- Number and type of pending ghost labs\n"
        "- Risk level (Low / Elevated / Critical) based on correlation of pending labs with active conditions and medications\n"
        "- Specific action items for the receiving clinician (PCP)\n"
        "- Medication reconciliation notes\n\n"
        "Use the available tools to retrieve real data — never fabricate clinical information. "
        "Present information clearly as if briefing a clinician during a care transition handoff. "
        "If FHIR context is not available, inform the caller they need to include it in their request."
    ),
    tools=[
        get_patient_demographics,
        get_active_medications,
        get_active_conditions,
        get_recent_observations,
    ],
    # Runs before every LLM call — extracts FHIR credentials from A2A
    # message metadata into session state so tools can query the FHIR server.
    before_model_callback=extract_fhir_context,
)
