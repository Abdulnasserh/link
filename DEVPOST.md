# Link: The Digital Bridge for Patient Transitions (Devpost Submission)

## 💡 Inspiration
Every year, millions of patients leave the hospital and enter a **"Post-Discharge Black Hole."** We were inspired by a staggering reality in 2026 healthcare:

*   **The Ticking Time Bomb**: Up to 100% of patients leave hospitals with "Pending Tests"—results that aren't finished when they check out. 40% of these "ghost results" are critical enough to change treatment, yet they are often missed because no one is assigned to watch a screen for a patient who has already gone home.
*   **The Medication Collision**: 60% of patients face medication errors during the transition from hospital to home, often taking duplicate or conflicting drugs.
*   **The Financial Stakes**: In FY 2026, the CMS has increased hospital readmission penalties, with 8% of all hospitals now facing a minimum 1% revenue penalty for failing to manage these transitions.

We built Link because "just calling the patient" isn't enough. We wanted to build a digital bridge that ensures no critical data—and no patient—is ever lost in transition again.

## 🚀 What it does
Link is an interoperable AI safety net that automates the "Last Mile" of patient discharge. It uses a specialized architecture to monitor, reconcile, and close the loop on patient care.

*   **The Digital Sentry (MCP)**: Link deploys an MCP (Model Context Protocol) Server that "stays behind" at the hospital. It continuously polls the FHIR server for any tests that were "Pending" at discharge. The moment a result turns "Final," Link’s intelligence analyzes it for clinical urgency.
*   **The Safety Reconciliation**: Link automatically compares the new hospital medications with the patient's existing home records (via FHIR MedicationRequest), flagging dangerous overlaps or omissions instantly.
*   **Contextual Intelligence (SHARP)**: Link uses the **SHARP** (Secure Healthcare Agent Resource Propagation) extension pattern to securely propagate patient IDs and FHIR tokens. It ensures that the family doctor receives a "Smart Brief" instead of a 20-page PDF, highlighting only the "Red Flags" and required actions.
*   **Closed-Loop Action**: Instead of a passive notification, Link generates clear, clinically-grounded summaries that lead to real-world medical action, ensuring "ghost results" are finally addressed.

## 🛠️ How we built it
We built Link with a focus on interoperability, security, and statelessness:
*   **Standardized Interoperability**: Built on **HL7 FHIR R4**, ensuring compatibility with major EHR providers like Epic, Cerner, and Google Cloud Healthcare API.
*   **Model Context Protocol (MCP)**: Leveraged **FastMCP** to create a secure, discovery-based toolset that agents can use to "see" into the hospital's data lake.
*   **SHARP Extension Pattern**: Implemented a custom capability patching system in the MCP server to support dynamic FHIR context injection (URLs and Bearer tokens) via metadata.
*   **Python Stack**: Used a modular Python architecture for the MCP server, with specialized tools for `DiagnosticReport`, `MedicationRequest`, and `Condition` resources.

## 🚧 Challenges we ran into
*   **FHIR Complexity**: Mapping nested and often inconsistent FHIR JSON resources into clean, concise snippets that an LLM can reason over without hitting token limits.
*   **Stateless Security**: Implementing the SHARP context propagation was challenging. We had to ensure that the MCP server never "stored" credentials but could still securely authenticate against the FHIR server for every request.
*   **Closing the Loop**: Designing the logic to differentiate between a "Normal" result and a "Red Flag" result that requires immediate PCP intervention.

## 🏆 Accomplishments that we're proud of
*   **True Interoperability**: Successfully querying live FHIR sandboxes and returning structured clinical intelligence.
*   **Zero-Trust Architecture**: Building a system where the AI never sees patient data unless the secure FHIR context is explicitly provided by the host platform.
*   **Impactful UX**: Moving beyond "AI Chat" to "AI Actions" by focusing on the 72-hour window where patient lives are most at risk.

## 📖 What we learned
*   **Standardization is Key**: MCP is the "missing link" for enterprise AI. It allows us to build medical tools once and deploy them across any AI platform.
*   **The Power of Small Tools**: We learned that specific, atomic tools (like `GetPendingLabs`) are much more effective for clinical safety than general-purpose "EHR search" tools.
*   **Agent Orchestration**: The transition from hospital to clinic isn't just a data transfer—it's a human handoff that requires an AI to act as a "Transition Specialist."

## 🔮 What's next for Link
*   **SMART on FHIR Launch**: Integrating Link directly into the clinician's workflow inside the EHR dashboard.
*   **Predictive Risk Scoring**: Using historical FHIR data to predict which patients are at the highest risk of readmission *before* they even leave the hospital.
*   **Patient-Facing Instructions**: Generating simple, multilingual discharge summaries that are automatically pushed to the patient's mobile device via secure channels.
