from mcp.server.fastmcp import FastMCP

from tools.pending_labs_tool import get_pending_labs
from tools.discharge_medications_tool import get_discharge_medications
from tools.active_conditions_tool import get_active_conditions
from tools.find_patient_tool import find_patient

mcp = FastMCP("Link Post-Discharge MCP", stateless_http=True, host="0.0.0.0")

# ── Patch capabilities to advertise FHIR context support ──────────────────────
# This tells the Prompt Opinion platform that our MCP needs FHIR context
# (server URL, bearer token, patient ID) to function.
_original_get_capabilities = mcp._mcp_server.get_capabilities


def _patched_get_capabilities(notification_options, experimental_capabilities):
    caps = _original_get_capabilities(notification_options, experimental_capabilities)
    caps.model_extra["extensions"] = {
        "ai.promptopinion/fhir-context": {
            "scopes": [
                {"name": "patient/Patient.rs", "required": True},
                {"name": "patient/DiagnosticReport.rs", "required": True},
                {"name": "patient/MedicationRequest.rs", "required": True},
                {"name": "patient/Condition.rs", "required": True},
            ]
        }
    }
    return caps


mcp._mcp_server.get_capabilities = _patched_get_capabilities

# ── Register tools ────────────────────────────────────────────────────────────
mcp.tool(
    name="GetPendingLabs",
    description="Fetches pending or preliminary diagnostic reports (ghost labs) that were ordered during a hospital stay but not finalized before discharge.",
)(get_pending_labs)

mcp.tool(
    name="GetDischargeMedications",
    description="Retrieves active medications for a patient to support medication reconciliation during care transitions.",
)(get_discharge_medications)

mcp.tool(
    name="GetActiveConditions",
    description="Retrieves the patient's active conditions and diagnoses, needed for post-discharge clinical risk assessment.",
)(get_active_conditions)

mcp.tool(
    name="FindPatient",
    description="Searches for a patient by name and returns their ID. Useful for identifying the correct patient context.",
)(find_patient)
