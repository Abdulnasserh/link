# 🔗 Link: Transition of Care Specialist

> **Resolving the "Post-Discharge Black Hole" with AI-Driven Clinical Intelligence.**

Link is a specialized AI agent designed to bridge the dangerous gap in patient care that occurs during the transition from hospital to home—a period often referred to as the "Post-Discharge Black Hole."

## 🚑 The Problem
Every year, thousands of patients are discharged from hospitals before all their laboratory results are finalized. These "ghost labs"—tests ordered in-patient but resulted post-discharge—frequently go unreviewed, leading to medication errors, missed diagnoses, and avoidable readmissions.

## 🛡️ The Solution: Link
Link acts as a **Transition of Care Specialist**. By leveraging the **Model Context Protocol (MCP)** and **FHIR (Fast Healthcare Interoperability Resources)**, Link proactively monitors a patient's health record during the critical 72-hour window after discharge.

Link doesn't just read data; it synthesizes it into clinical intelligence for the receiving primary care physician (PCP).

### Key Capabilities
- **👻 Ghost Lab Detection**: Identifies pending or preliminary diagnostic reports that were ordered during a hospital stay but not finalized before discharge.
- **💊 Medication Reconciliation**: Correlates discharge medications with the patient's active condition list to identify potential conflicts or gaps.
- **⚠️ Risk Stratification**: Assesses the clinical risk level (Low, Elevated, or Critical) by correlating pending results with the patient's existing diagnoses.
- **📋 Clinical Handover**: Generates structured, clinician-ready reports for PCPs, ensuring no critical data falls through the cracks.

---

## 🏗️ Technical Architecture

Link is built on a modular, secure, and interoperable stack designed for modern healthcare environments.

### 1. Link MCP Server (`/mcp_server`)
Built using **FastMCP**, this component acts as the secure gateway to the hospital's FHIR server.
- **FHIR Integration**: Uses a custom-patched capability set to support the `ai.promptopinion/fhir-context` extension. This allows for dynamic injection of FHIR server URLs, bearer tokens, and patient IDs via A2A (Agent-to-Agent) metadata.
- **Clinical Tools**:
  - `GetPendingLabs`: Queries `DiagnosticReport` resources for non-finalized results.
  - `GetDischargeMedications`: Fetches `MedicationRequest` resources.
  - `GetActiveConditions`: Retrieves `Condition` resources for clinical context.

### 2. Link Agent (`/link_agent`)
The brain of the system, built using the **Google Agent Development Kit (ADK)**.
- **Reasoning Engine**: Powered by Gemini (via LiteLLM), Link follows a strict clinical workflow:
  1. Identity confirmation.
  2. Diagnostic report auditing.
  3. Medication reconciliation.
  4. Diagnostic correlation.
  5. Structured synthesis.
- **Context Awareness**: Uses a `before_model_callback` to extract FHIR credentials from incoming message metadata, ensuring zero-trust security and stateless operation.

---

## 🛠️ How it Works (Simply)

1. **Context Injection**: When a request is made to Link (e.g., from the Prompt Opinion platform), the patient's FHIR credentials are encrypted and passed in the metadata.
2. **Dynamic Discovery**: Link's MCP server advertises its need for FHIR context. The platform provides this context, which Link's agent then uses to authenticate against the electronic health record (EHR).
3. **Tool Execution**: The agent calls specialized tools to pull specific medical data.
4. **Clinical Synthesis**: Link processes the raw FHIR data (which is often messy and nested) and turns it into a human-readable handover report.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Access to a FHIR R4 server (or a sandbox like Epic/Cerner)
- Google AI Studio API Key (for Gemini)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Abdulnasserh/link.git
   ```
2. Install dependencies for the MCP server:
   ```bash
   cd mcp_server
   pip install -r requirements.txt
   ```
3. Install dependencies for the Agent:
   ```bash
   cd ../link_agent
   pip install -r requirements.txt
   ```

---

## 👨‍⚖️ For the Judges
Link represents the future of interoperable healthcare AI. By combining the **Model Context Protocol** with **HL7 FHIR standards**, we have created an agent that is:
- **Scalable**: Works across any hospital system that supports FHIR.
- **Secure**: Uses metadata-based credential injection rather than hardcoded keys.
- **Clinically Relevant**: Solves a specific, high-cost problem in the US healthcare system (Transition of Care).

Built with ❤️ for the **Prompt Opinion / MCP Hackathon**.
