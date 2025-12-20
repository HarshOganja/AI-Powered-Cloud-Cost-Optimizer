# Cloud Cost Optimizer
AI-Powered Cloud Cost Optimization Tool using Large Language Models

## Overview

Cloud Cost Optimizer is a CLI-based application that uses Large Language Models (LLMs) to analyze cloud project requirements, generate realistic synthetic billing data, perform budget-aware cost analysis, and provide actionable multi-cloud cost optimization recommendations.  
The system also produces structured JSON outputs and a professional HTML report for easy review.

---

## Key Capabilities

### Project Profile Extraction
- Converts natural language project descriptions into structured project metadata  
- Extracts budget, technology stack, and non-functional requirements  
- Strict JSON output validation  

### Synthetic Billing Generation
- Generates realistic, cloud-agnostic billing records  
- Budget-aware cost distribution  
- One service per responsibility for clean billing  

### Cost Analysis
- Calculates total monthly cost  
- Compares cost against budget  
- Identifies high-cost services and budget variance  

### Cost Optimization Recommendations
- Generates 6–10 actionable recommendations  
- Covers multi-cloud options (AWS, Azure, GCP) and open-source alternatives  
- Includes potential savings, implementation effort, and risk level  

### Reporting
- Structured JSON reports  
- Professional HTML report for human-readable analysis  
- CLI-based export workflow  

### CLI Orchestrator
- Menu-driven command-line interface  
- Executes the complete pipeline step by step  

---

## High-Level Workflow

1. User enters project description in plain English  
2. LLM extracts structured project profile  
3. LLM generates synthetic cloud billing data  
4. Cost analysis evaluates billing against budget  
5. LLM generates optimization recommendations  
6. Reports are exported in JSON and HTML formats  

---

## Project Structure


```
AI-POWERED-CLOUD-COST-OPTIMIZER/
│
├── data/
│   ├── input/
│   │   └── sample_project_profile.txt
│   └── output/
│       ├── Profile_Extraction.json
│       ├── Billing_Generation.json
│       ├── Recommendation.json
│       ├── cost_optimization_report.json
│       └── cost_optimization_report.html
│
├── src/
│   ├── Profile_Extraction.py
│   ├── Bill_Genration.py
│   ├── Recommendation.py
│   └── Html_Report.py
│
├── LLM_Cost_Optimizer.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Technology Stack

| Component | Technology |
|---------|------------|
| Language | Python 3.10+ |
| LLM API | Hugging Face Inference API |
| LLM Model | Meta-Llama-3-8B-Instruct |
| Environment Management | python-dotenv |
| HTTP Client | requests |
| Interface | CLI (Python) |


## Installation and Setup

1. Clone the repository  
```
git clone <repository-url>
cd AI-POWERED-CLOUD-COST-OPTIMIZER
```

2. Create and activate virtual environment  

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies  
```
pip install -r dependency.txt
```

4. Configure environment variables  

### ⚙️Configuration

1️⃣ Get HuggingFace API Key

- Sign up at HuggingFace
- Go to Settings → Access Tokens
- Click "New token" with Read access
- Copy your token (starts with hf\_)


Create a `.env` file:
```
HF_API_KEY=your_huggingface_api_key
```

---

## Usage

Run the CLI orchestrator:
```
python LLM_Cost_Optimizer.py

```

---

# MAIN MENU

```
================ Cloud Cost Optimizer =================
1. Enter new project description and extract profile
2. Generate synthetic billing and cost analysis
3. Generate optimization recommendations
4. Export full report as JSON and HTML
5. Exit
======================================================
```
## Output Files

Generated in `data/output/`:
- Profile_Extraction.json  
- Billing_Generation.json  
- Recommendation.json  
- cost_optimization_report.json  
- cost_optimization_report.html  

---

## Design Principles

- Modular architecture  
- Strict JSON-only LLM outputs  
- Budget-aware cost modeling  
- Cloud-provider consistency  

---

---

## AI Tool Usage Disclosure

ChatGPT was used as a development assistance tool for:
- Prompt design and refinement  
- Structuring strict JSON schemas  
- Improving error handling logic  
- Assisting with HTML report generation  

All final implementation and integration decisions were made by the author.

---


## Author

Harsh Oganja  
Email: harshoganja@gmail.com  
GitHub: https://github.com/HarshOganja  
Project Repository: https://github.com/HarshOganja/AI-Powered-Cloud-Cost-Optimizer.git
---

