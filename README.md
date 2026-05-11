# 🔗 Link: Post-Discharge Clinical MCP Server

> **Interoperable Medical Superpowers for AI Agents via FHIR.**

The Link MCP Server is a specialized medical toolset designed to resolve the "Post-Discharge Black Hole"—the dangerous gap in care that occurs when patients leave the hospital before all lab results are finalized.

## 🚑 The Problem: "Ghost Labs"
Every year, thousands of patients are discharged from hospitals before all their laboratory results are finalized. These "ghost labs" frequently go unreviewed, leading to medication errors, missed diagnoses, and avoidable readmissions.

## 🛡️ The Solution
This Model Context Protocol (MCP) server exposes secure, read-only clinical tools that allow any compatible AI agent to bridge this gap by querying live **FHIR (Fast Healthcare Interoperability Resources)** data.

### Key Tools
- **👻 GetPendingLabs**: Identifies pending or preliminary diagnostic reports (`DiagnosticReport`) that were ordered during a hospital stay but not finalized before discharge.
- **💊 GetDischargeMedications**: Retrieves active medications (`MedicationRequest`) for a patient to support medication reconciliation during care transitions.
- **📋 GetActiveConditions**: Retrieves the patient's active diagnoses (`Condition`), essential for clinical risk assessment.

---

## 🏗️ Technical Architecture

Built using **FastMCP**, this server is designed for high-stakes healthcare environments:

- **Context-Aware Security**: Uses a patched capability set to support the `ai.promptopinion/fhir-context` extension. This allows the host platform to dynamically inject FHIR server URLs and bearer tokens via metadata, ensuring the server remains stateless and secure.
- **FHIR R4 Interoperability**: Built to query standard HL7 FHIR resources, making it compatible with major EHR systems like Epic, Cerner, and Google Cloud Healthcare API.
- **Stateless Operation**: No patient data is stored on the MCP server; it acts as a real-time bridge between the AI and the health record.

---

## 🛠️ How it Works (Simply)

1. **Discovery**: The MCP server advertises its clinical capabilities and its requirement for FHIR context (URL/Token).
2. **Context Injection**: When an agent calls a tool, the host platform (like Prompt Opinion) injects the patient's secure FHIR credentials into the request metadata.
3. **FHIR Querying**: The server uses these credentials to perform real-time searches against the hospital's FHIR server.
4. **Data Synthesis**: The server processes raw, complex FHIR JSON and returns clean, clinically relevant snippets to the AI agent.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Access to a FHIR R4 server (or sandbox)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Abdulnasserh/link.git
   ```
2. Install dependencies:
   ```bash
   cd mcp_server
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python mcp_server/main.py
   ```

---

## 👨‍⚖️ For the Judges
The Link MCP Server demonstrates how **Standardized Interoperability (FHIR)** combined with **Standardized Tooling (MCP)** can solve critical, high-cost healthcare problems. By providing agents with the "eyes" to see pending labs and medications, we can prevent medical errors and improve patient safety during the most vulnerable 72 hours after hospital discharge.

Built with ❤️ for the **Prompt Opinion / MCP Hackathon**.
