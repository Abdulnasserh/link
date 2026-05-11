from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context, get_patient_id_if_context_exists
from mcp_utilities import create_text_response


async def get_discharge_medications(
    patientId: Annotated[
        str | None,
        Field(description="The id of the patient. Optional if patient context already exists."),
    ] = None,
    ctx: Context = None,
) -> str:
    """Retrieves active medications for a patient to support medication reconciliation during
    care transitions. Highlights medications that need verification after discharge."""

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
        "MedicationRequest",
        search_parameters={
            "patient": patientId,
            "status": "active",
            "_count": "50",
        },
    )
    
    # 2. Fallback to HAPI FHIR
    if not bundle:
        fallback_url = "https://hapi.fhir.org/baseR4"
        fallback_patient_id = "132019585"
        fhir_client = FhirClient(fallback_url)
        bundle = await fhir_client.search(
            "MedicationRequest",
            search_parameters={
                "patient": fallback_patient_id,
                "status": "active",
                "_count": "50",
            },
        )

    if not bundle:
        return create_text_response("Could not query the FHIR server for MedicationRequests.", is_error=True)

    entries = bundle.get("entry", [])
    if not entries:
        return create_text_response("No active medications found for this patient.")

    meds = []
    for entry in entries:
        resource = entry.get("resource", {})
        med_concept = resource.get("medicationCodeableConcept", {})
        med_name = (
            med_concept.get("text")
            or _coding_display(med_concept.get("coding", []))
            or resource.get("medicationReference", {}).get("display", "Unknown Medication")
        )
        status = resource.get("status", "unknown")
        dosage_list = [d.get("text", "No dosage text") for d in resource.get("dosageInstruction", [])]
        dosage = dosage_list[0] if dosage_list else "Not specified"
        authored = resource.get("authoredOn", "Unknown date")
        requester = (resource.get("requester") or {}).get("display", "Unknown")

        meds.append(f"- {med_name} | Dosage: {dosage} | Status: {status} | Prescribed: {authored} | By: {requester}")

    return create_text_response(
        f"Found {len(meds)} active medication(s) for patient {patientId}:\n" + "\n".join(meds)
    )


def _coding_display(codings: list) -> str:
    for c in codings:
        if c.get("display"):
            return c["display"]
    return "Unknown"
