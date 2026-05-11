#!/usr/bin/env python3
"""
Seed script — creates a demo patient on the public HAPI FHIR R4 sandbox
with realistic post-discharge data:
  - Patient demographics
  - 3 pending "ghost labs" (DiagnosticReport with status=preliminary/registered)
  - 4 active medications
  - 3 active conditions

Run:
    pip install httpx
    python scripts/seed_demo_data.py

After running, note the Patient ID printed at the end — you'll use it in
the Prompt Opinion platform to demo Link.
"""

import httpx
import json
import sys

FHIR_BASE = "https://hapi.fhir.org/baseR4"
HEADERS = {"Content-Type": "application/fhir+json", "Accept": "application/fhir+json"}


def post_resource(resource: dict) -> dict:
    """POST a FHIR resource and return the created resource with its ID."""
    resource_type = resource["resourceType"]
    resp = httpx.post(f"{FHIR_BASE}/{resource_type}", json=resource, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    created = resp.json()
    print(f"  ✓ Created {resource_type}/{created['id']}")
    return created


def main():
    print("🏥 Seeding HAPI FHIR sandbox with Link demo data...\n")

    # ── 1. Patient ─────────────────────────────────────────────────────────
    print("1/4  Creating patient...")
    patient = post_resource({
        "resourceType": "Patient",
        "active": True,
        "name": [
            {
                "use": "official",
                "family": "Rivera",
                "given": ["Maria", "Elena"],
            }
        ],
        "gender": "female",
        "birthDate": "1958-03-14",
        "telecom": [
            {"system": "phone", "value": "+1-555-867-5309", "use": "mobile"},
            {"system": "email", "value": "maria.rivera@example.com"},
        ],
        "address": [
            {
                "use": "home",
                "line": ["742 Evergreen Terrace"],
                "city": "Springfield",
                "state": "IL",
                "postalCode": "62704",
                "country": "US",
            }
        ],
        "maritalStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus", "code": "M"}],
            "text": "Married",
        },
    })
    patient_id = patient["id"]

    # ── 2. Active Conditions ───────────────────────────────────────────────
    print("\n2/4  Creating active conditions...")
    conditions = [
        {
            "resourceType": "Condition",
            "subject": {"reference": f"Patient/{patient_id}"},
            "clinicalStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
            },
            "verificationStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]
            },
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "73211009", "display": "Diabetes mellitus"}],
                "text": "Type 2 Diabetes Mellitus",
            },
            "severity": {"text": "Moderate"},
            "onsetDateTime": "2019-06-15",
            "recordedDate": "2019-06-15",
        },
        {
            "resourceType": "Condition",
            "subject": {"reference": f"Patient/{patient_id}"},
            "clinicalStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
            },
            "verificationStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]
            },
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertensive disorder"}],
                "text": "Essential Hypertension",
            },
            "severity": {"text": "Mild"},
            "onsetDateTime": "2020-01-10",
            "recordedDate": "2020-01-10",
        },
        {
            "resourceType": "Condition",
            "subject": {"reference": f"Patient/{patient_id}"},
            "clinicalStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
            },
            "verificationStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]
            },
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "431855005", "display": "Chronic kidney disease stage 3"}],
                "text": "Chronic Kidney Disease Stage 3",
            },
            "severity": {"text": "Moderate"},
            "onsetDateTime": "2022-09-01",
            "recordedDate": "2022-09-01",
        },
    ]
    for cond in conditions:
        post_resource(cond)

    # ── 3. Active Medications ──────────────────────────────────────────────
    print("\n3/4  Creating active medications...")
    medications = [
        {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "subject": {"reference": f"Patient/{patient_id}"},
            "medicationCodeableConcept": {
                "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "860975", "display": "Metformin 500mg"}],
                "text": "Metformin 500mg",
            },
            "dosageInstruction": [{"text": "500mg twice daily with meals"}],
            "authoredOn": "2024-11-15",
            "requester": {"display": "Dr. Sarah Chen"},
        },
        {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "subject": {"reference": f"Patient/{patient_id}"},
            "medicationCodeableConcept": {
                "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "314076", "display": "Lisinopril 10mg"}],
                "text": "Lisinopril 10mg",
            },
            "dosageInstruction": [{"text": "10mg once daily in the morning"}],
            "authoredOn": "2024-11-15",
            "requester": {"display": "Dr. Sarah Chen"},
        },
        {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "subject": {"reference": f"Patient/{patient_id}"},
            "medicationCodeableConcept": {
                "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "1049221", "display": "Warfarin 5mg"}],
                "text": "Warfarin 5mg",
            },
            "dosageInstruction": [{"text": "5mg once daily at bedtime — INR target 2.0-3.0"}],
            "authoredOn": "2026-05-01",
            "requester": {"display": "Dr. James Okonkwo (Hospitalist)"},
        },
        {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "subject": {"reference": f"Patient/{patient_id}"},
            "medicationCodeableConcept": {
                "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "310429", "display": "Furosemide 40mg"}],
                "text": "Furosemide 40mg",
            },
            "dosageInstruction": [{"text": "40mg once daily in the morning"}],
            "authoredOn": "2026-05-01",
            "requester": {"display": "Dr. James Okonkwo (Hospitalist)"},
        },
    ]
    for med in medications:
        post_resource(med)

    # ── 4. Ghost Labs (pending DiagnosticReports) ──────────────────────────
    print("\n4/4  Creating ghost labs (pending DiagnosticReports)...")
    ghost_labs = [
        {
            "resourceType": "DiagnosticReport",
            "status": "preliminary",
            "subject": {"reference": f"Patient/{patient_id}"},
            "code": {
                "coding": [{"system": "http://loinc.org", "code": "6690-2", "display": "WBC"}],
                "text": "Complete Blood Count (CBC) with Differential",
            },
            "category": [
                {
                    "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "HM"}],
                    "text": "Hematology",
                }
            ],
            "effectiveDateTime": "2026-05-06T14:30:00Z",
        },
        {
            "resourceType": "DiagnosticReport",
            "status": "registered",
            "subject": {"reference": f"Patient/{patient_id}"},
            "code": {
                "coding": [{"system": "http://loinc.org", "code": "4548-4", "display": "HbA1c"}],
                "text": "Hemoglobin A1c (HbA1c)",
            },
            "category": [
                {
                    "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "CH"}],
                    "text": "Chemistry",
                }
            ],
            "effectiveDateTime": "2026-05-06T09:00:00Z",
        },
        {
            "resourceType": "DiagnosticReport",
            "status": "preliminary",
            "subject": {"reference": f"Patient/{patient_id}"},
            "code": {
                "coding": [{"system": "http://loinc.org", "code": "34714-6", "display": "INR"}],
                "text": "INR / Coagulation Panel",
            },
            "category": [
                {
                    "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "HM"}],
                    "text": "Hematology",
                }
            ],
            "effectiveDateTime": "2026-05-07T08:15:00Z",
        },
    ]
    for lab in ghost_labs:
        post_resource(lab)

    # ── Summary ────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("✅ Demo data seeded successfully!")
    print("=" * 60)
    print(f"\n  Patient:   Maria Elena Rivera")
    print(f"  Patient ID: {patient_id}")
    print(f"  FHIR URL:  {FHIR_BASE}")
    print(f"\n  Conditions:  3 active (Diabetes, Hypertension, CKD Stage 3)")
    print(f"  Medications: 4 active (Metformin, Lisinopril, Warfarin, Furosemide)")
    print(f"  Ghost Labs:  3 pending (CBC, HbA1c, INR)")
    print(f"\n  ⚠  RISK HIGHLIGHT: Patient is on Warfarin with a pending INR")
    print(f"     result. This is a CRITICAL ghost lab that Link should flag.")
    print(f"\n  Use this Patient ID in the Prompt Opinion platform to demo Link.")
    print(f"  FHIR server: {FHIR_BASE} (no auth token needed for HAPI sandbox)")


if __name__ == "__main__":
    main()
