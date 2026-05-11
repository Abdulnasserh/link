from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context, get_patient_id_if_context_exists
from mcp_utilities import create_text_response


async def get_pending_labs(
    patientId: Annotated[
        str | None,
        Field(description="The id of the patient. Optional if patient context already exists."),
    ] = None,
    ctx: Context = None,
) -> str:
    """Fetches pending or preliminary DiagnosticReport resources (ghost labs) for a patient.
    These are lab results ordered during a hospital stay that were not finalized before discharge."""

    if not patientId:
        patientId = get_patient_id_if_context_exists(ctx)
        if not patientId:
            raise ValueError("No patient context found")

    fhir_context = get_fhir_context(ctx)
    if not fhir_context:
        raise ValueError("The FHIR context could not be retrieved")

    # 1. Try with the provided context (Prompt Opinion FHIR)
    fhir_client = FhirClient(base_url=fhir_context.url, token=fhir_context.token)
    bundle = await fhir_client.search(
        "DiagnosticReport",
        search_parameters={
            "patient": patientId,
            "status": "registered,partial,preliminary",
            "_count": "50",
            "_sort": "-date",
        },
    )

    if not bundle:
        return create_text_response("Could not query the FHIR server for DiagnosticReports.", is_error=True)

    entries = bundle.get("entry", [])
    if not entries:
        return create_text_response("No pending ghost labs found for this patient.")

    labs = []
    for entry in entries:
        resource = entry.get("resource", {})
        code = resource.get("code", {})
        code_text = code.get("text") or _coding_display(code.get("coding", []))
        status = resource.get("status", "unknown")
        issued = resource.get("issued", "Not yet issued")
        effective = resource.get("effectiveDateTime", "Unknown date")
        category_list = resource.get("category", [])
        category = category_list[0].get("text", "Uncategorized") if category_list else "Uncategorized"

        labs.append(f"- {code_text} | Status: {status} | Category: {category} | Effective: {effective} | Issued: {issued}")

    return create_text_response(
        f"Found {len(labs)} pending 'ghost' lab(s) for patient {patientId}:\n" + "\n".join(labs)
    )


def _coding_display(codings: list) -> str:
    for c in codings:
        if c.get("display"):
            return c["display"]
    return "Unknown Lab Type"
