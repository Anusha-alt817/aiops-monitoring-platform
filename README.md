# AI-Powered DevOps Monitoring Platform

An end-to-end AIOps project that monitors a banking application, detects abnormal behavior, analyzes incidents, retrieves historical troubleshooting knowledge, and generates AI-assisted incident investigation reports.

## Project Overview

This project combines traditional DevOps monitoring with Generative AI to improve incident detection and troubleshooting.

It uses Prometheus and Grafana for monitoring, Python for anomaly detection and incident processing, ChromaDB for vector storage, LangChain and LlamaIndex for RAG retrieval, and Amazon Bedrock for AI-powered incident analysis.

## Architecture

Banking Application -> Flask APIs -> Prometheus -> Grafana

Python AIOps Engine -> Anomaly Detection + Log Analysis -> Incident Reports

Incident Knowledge -> ChromaDB Vector Database
                         |
              +----------+----------+
              |                     |
          LangChain             LlamaIndex
              |                     |
              +------ RAG Retrieval-+
                         |
                  Incident Context
                         |
              LangChain + Amazon Bedrock
                         |
              AI Incident Investigation
                         |
                  Markdown Reports

## Technology Stack

| Category | Technologies |
|---|---|
| Cloud | AWS EC2 |
| Application | Python, Flask |
| Containers | Docker |
| Monitoring | Prometheus, Grafana, Node Exporter |
| Automation | Python, Bash |
| AI Frameworks | LangChain, LlamaIndex |
| Generative AI | Amazon Bedrock, Claude Haiku 4.5 |
| RAG | Retrieval-Augmented Generation |
| Vector Database | ChromaDB |
| Embeddings | ChromaDB Default Embedding Function |
| Version Control | Git, GitHub |
| Operating System | Ubuntu Linux |

## Key Features

1. Application and infrastructure monitoring.
2. Python-based anomaly detection.
3. Application log analysis.
4. Automated incident report generation.
5. Historical incident knowledge management.
6. ChromaDB vector ingestion and semantic retrieval.
7. LangChain-based RAG pipeline.
8. LlamaIndex-based RAG retrieval using the same ChromaDB collection.
9. LangChain vs. LlamaIndex retrieval comparison using identical questions.
10. Amazon Bedrock AI-assisted incident analysis.
11. Markdown incident report generation.

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Banking application home |
| `/health` | Application health check |
| `/transactions` | Transaction API |
| `/slow` | Simulate slow API response |
| `/simulate-error` | Simulate HTTP 500 error |
| `/metrics` | Prometheus metrics endpoint |

## Incident Investigation Workflow

1. Prometheus collects application and infrastructure metrics.
2. Grafana visualizes monitoring data.
3. Python scripts analyze metrics and application logs.
4. The AIOps pipeline generates incident reports.
5. Historical incidents are stored in the knowledge base.
6. ChromaDB retrieves relevant troubleshooting documents.
7. LangChain and LlamaIndex retrieve relevant incident knowledge from the shared ChromaDB collection.
8. Both frameworks are compared using the same incident question and top-three retrieval results.
9. LangChain combines incident questions with retrieved context.
10. Amazon Bedrock generates AI-assisted investigation results.
11. The report writer saves analysis as Markdown reports.

## Safety and Reliability

- AI recommendations are advisory, not automatic remediation.
- Human validation is required before corrective action.
- AWS credentials are managed outside the source repository.
- Generated reports, virtual environments, and vector database files are excluded from Git.

## Project Structure

- `aiops/` - Monitoring, anomaly detection, incident analysis, and RAG scripts
- `application/` - Flask banking application and Docker configuration
- `monitoring/` - Prometheus configuration
- `knowledge_base/incidents/` - Historical incident documents
- `knowledge_base/runbooks/` - Troubleshooting documentation
- `reports/` - Generated incident reports

## Current Implementation Status

- Infrastructure and application monitoring implemented.
- Python anomaly detection and log analysis implemented.
- Automated incident reporting implemented.
- ChromaDB ingestion and retrieval implemented.
- LangChain RAG integration implemented.
- LlamaIndex RAG integration implemented.
- LangChain vs. LlamaIndex retrieval comparison completed using shared ChromaDB storage.
- Amazon Bedrock incident analysis tested.
- Markdown report generation tested with sample data.

## Future Enhancements

- Demonstrate GitHub Copilot and Amazon Q Developer.
- Improve incident classification and root cause analysis.
- Add CI/CD automation for application deployment.
- Expand the knowledge base with troubleshooting runbooks.

## Author

**Anusha NallagonDa**

GitHub: https://github.com/Anusha-alt817

Project: AI-Powered DevOps Monitoring Platform
