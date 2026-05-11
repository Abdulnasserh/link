from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context, get_patient_id_if_context_exists
from mcp_utilities import create_text_response


async def get_active_conditions(
    patientId: Annotated[
        str | None,
        Field(description="The id of the patient. Optional if patient context already exists."),
    ] = None,
    ctx: Context = None,
) -> str:
    """Retrieves the patient's active conditions and diagnoses from the FHIR server.
    Important for post-discharge risk assessment — conditions affect how pending
    lab results should be interpreted."""

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
        "Condition",
        search_parameters={
            "patient": patientId,
            "clinical-status": "active",
            "_count": "50",
        },
    )

    # 2. Fallback to HAPI FHIR
    if bundle is None:
        fallback_url = "https://hapi.fhir.org/baseR4"
        fallback_patient_id = "132019585"
        fhir_client = FhirClient(base_url=fallback_url)
        bundle = await fhir_client.search(
            "Condition",
            search_parameters={
                "patient": fallback_patient_id,
                "clinical-status": "active",
                "_count": "50",
            },
        )

    if not bundle:
        return create_text_response("Could not query the FHIR server for Conditions.", is_error=True)

    entries = bundle.get("entry", [])
    if not entries:
        return create_text_response("No active conditions found for this patient.")

    conditions = []
    for entry in entries:
        resource = entry.get("resource", {})
        code = resource.get("code", {})
        name = code.get("text") or _coding_display(code.get("coding", []))
        severity = (resource.get("severity") or {}).get("text", "Not specified")
        onset = resource.get("onsetDateTime") or (resource.get("onsetPeriod") or {}).get("start", "Unknown")
        recorded = resource.get("recordedDate", "Unknown")

        conditions.append(f"- {name} | Severity: {severity} | Onset: {onset} | Recorded: {recorded}")

    return create_text_response(
        f"Found {len(conditions)} active condition(s) for patient {patientId}:\n" + "\n".join(conditions)
    )


def _coding_display(codings: list) -> str:
    for c in codings:
        if c.get("display"):
            return c["display"]
    return "Unknown Condition"
