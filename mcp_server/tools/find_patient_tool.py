from typing import Annotated
from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context
from mcp_utilities import create_text_response


async def find_patient(
    name: Annotated[str, Field(description="The name of the patient to search for (e.g., 'Maria Rivera').")],
    ctx: Context = None,
) -> str:
    """Searches for a patient by name in the FHIR server and returns their Patient ID."""
    
    fhir_context = get_fhir_context(ctx)
    if not fhir_context:
        return create_text_response("No FHIR context found. Please ensure context is injected.", is_error=True)

    fhir_client = FhirClient(base_url=fhir_context.url, token=fhir_context.token)
    
    # Search for patient by name
    bundle = await fhir_client.search(
        "Patient",
        search_parameters={
            "name": name,
            "_count": "5",
        },
    )

    if not bundle:
        return create_text_response(f"Could not query the FHIR server for patient: {name}", is_error=True)

    entries = bundle.get("entry", [])
    if not entries:
        return create_text_response(f"No patient found matching name: {name}")

    results = []
    for entry in entries:
        resource = entry.get("resource", {})
        patient_id = resource.get("id")
        names = resource.get("name", [])
        name_str = "Unknown"
        if names:
            name_parts = names[0].get("given", []) + [names[0].get("family", "")]
            name_str = " ".join(filter(None, name_parts))
        
        results.append(f"- Name: {name_str} | Patient ID: {patient_id}")

    return create_text_response(
        f"Found {len(results)} patient(s) matching '{name}':\n" + "\n".join(results)
    )
