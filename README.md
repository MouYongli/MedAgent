# MedAgent: Medical Guidelines Recommendation System Based on Retrieval Augmented Retrieval and Agentic AI Workflows

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.4-green)](https://developer.nvidia.com/cuda-downloads)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5.0-red)](https://pytorch.org/get-started/locally/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[![Forks](https://img.shields.io/github/forks/MouYongli/MedAgent?style=social)](https://github.com/MouYongli/MedAgent/network/members)
[![Stars](https://img.shields.io/github/stars/MouYongli/MedAgent?style=social)](https://github.com/MouYongli/MedAgent/stargazers)
[![Issues](https://img.shields.io/github/issues/MouYongli/MedAgent)](https://github.com/MouYongli/MedAgent/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/MouYongli/MedAgent)](https://github.com/MouYongli/MedAgent/pulls)
[![Contributors](https://img.shields.io/github/contributors/MouYongli/MedAgent)](https://github.com/MouYongli/MedAgent/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/MouYongli/MedAgent)](https://github.com/MouYongli/MedAgent/commits/main)
<!-- [![Build Status](https://img.shields.io/github/actions/workflow/status/MouYongli/MedAgent/ci.yml)](https://github.com/MouYongli/MedAgent/actions)
[![Code Quality](https://img.shields.io/lgtm/grade/python/g/MouYongli/MedAgent.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MouYongli/MedAgent/context:python) -->

[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://hub.docker.com/r/YOUR_DOCKER_IMAGE)
[![Colab](https://img.shields.io/badge/Open%20in-Colab-yellow)](https://colab.research.google.com/github/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/blob/main/notebooks/demo.ipynb)
[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxx)


[![WeChat](https://img.shields.io/badge/WeChat-公众号名称-green)](https://your-wechat-link.com)
[![Weibo](https://img.shields.io/badge/Weibo-关注-red)](https://weibo.com/YOUR_WEIBO_LINK)
<!-- [![Discord](https://img.shields.io/discord/YOUR_DISCORD_SERVER_ID?label=Discord&logo=discord&color=5865F2)](https://discord.gg/YOUR_INVITE_LINK) -->
<!-- [![Twitter](https://img.shields.io/twitter/follow/YOUR_TWITTER_HANDLE?style=social)](https://twitter.com/YOUR_TWITTER_HANDLE) -->



This is official repo for "MedAgent: **Med**ical Guidelines Recommendation System Based on Retrieval Augmented Retrieval and **Agent**ic AI Workflows" by DBIS at RWTH Aachen University
([Yongli Mou*](mou@dbis.rwth-aachen.de), Hanbin Chen, Meret Unbehaun, Saif Nasir and Stefan Decker) and University Hospital Aachen (Nadine Önelmis and Behrus Puladi)

## Overview

The Medical Guidelines Recommendation System (MedAgent) is an advanced AI-powered solution designed to assist healthcare professionals in making informed medical decisions by providing personalized, evidence-based medical guidelines. This system leverages the capabilities of Large Language Models (LLMs) and Agentic AI workflows to create a robust framework for dynamic interaction between users (doctors) and the system, and to facilitate continuous learning and adaptation through a Retrieve-and-Generate (RAG) pipeline.


## Features
- **Large Language Models (LLMs)**: At the core of the system, LLMs such as GPT-based models are utilized to understand medical queries and generate responses in natural language, ensuring that recommendations are presented in an intuitive, easy-to-understand format for doctors.

- **Agentic AI Workflow**: This component enables the system to perform complex tasks autonomously. It orchestrates the interaction between different models and databases, ensuring a smooth process for retrieving relevant medical guidelines, processing them, and providing actionable insights. The agentic behavior allows the system to adapt to different contexts based on user input and system status.

- **RAG Pipeline**: The system integrates the Retrieve-and-Generate (RAG) pipeline, which enables it to query relevant databases for up-to-date medical information. This includes using retrieval-based techniques to extract the most relevant data from external sources (e.g., medical research, guidelines databases) and then generating personalized recommendations or explanations for the doctor.

Role-based Interactions: The system is designed to serve two primary user roles:

- **Doctors (End-users)**: They interact with the system to receive medical recommendations, guidelines, and insights based on patient data and clinical queries.
- **Knowledge Maintainers (Developers)**: These users are responsible for keeping the system's knowledge base up to date, ensuring that medical guidelines and AI models are regularly improved and trained to handle emerging medical trends and innovations.


## Components

- Frontend (Next.js): The user interface is built with Next.js, providing a modern, responsive, and fast application where doctors can input queries, review recommendations, and interact with the AI-powered assistant. The frontend communicates with the backend to handle the logic and AI operations.

- Backend (FastAPI): The backend is built with FastAPI, handling API requests, interacting with databases, running AI models, and serving the AI-generated guidelines and recommendations to the frontend.
  
- Databases:
  - MongoDB and Postgres is used to store and manage study data, user interactions, and structured medical data.
  - Neo4j (Graph Database) is used for knowledge representation, allowing the system to model medical relationships, such as drug interactions or disease pathways.
  - Vector Database (e.g., FAISS or similar) is employed to store and query embeddings of medical guidelines and knowledge for efficient retrieval.

- Authentication & Security: The system uses Keycloak for secure authentication and user management. This ensures that only authorized personnel (e.g., doctors and developers) can access the system and modify sensitive data.

- **Notebooks** is temporarily added as a start for trying out the backend API and demonstrating the intended study performed during the interactive development proces


## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Conda package manager
- npm package manager

### Quick Start

We provide a convenient script to start both frontend and backend services simultaneously:

```bash
# Add execution permission
chmod +x start.sh

# Run the script
./start.sh
```

The script will automatically:
- Check for required dependencies
- Create and activate conda environment (if not exists)
- Install required dependencies
- Start backend service (http://127.0.0.1:8000)
- Start frontend service (http://localhost:3000)

You can use `Ctrl+C` to stop all services at once.

### Manual Deployment

If you prefer to control the deployment process manually, follow these steps:

#### Backend Setup

1. Create and activate Conda environment
```bash
# Create environment
conda create --name medagent python=3.10

# Activate environment
conda activate medagent

# Navigate to backend directory
cd backend

# Install dependencies
pip install -e .
```

2. Start backend service
```bash
# Start in development mode (with hot reload)
python -m uvicorn app.main:app --reload
```

The service will run at http://127.0.0.1:8000

#### Frontend Setup

1. Install dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

2. Start development server
```bash
npm run dev
```

The frontend will run at http://localhost:3000

### Docker-compose

## Datasets

## Usage

Here's an example of how to use the model:

```python
from api.llms.azure import AzureChatCompletion
llm = AzureChatCompletion(azure_endpoint="https:your_endpoint.azure.com", azure_deployment="your_deployment_name", azure_api="your_azure_api", azure_api_version="your_api_version")
```

More detailed tutorials can be found in our [documentation](https://your-project-website.com/docs).

## Project Structure

```
📦 MedAgent
├── 📁 docs                # Documentation and API references
├── 📁 frontend     
├── 📁 backend         
├── 📁 docker        
│   ├── 📁 keycloak  
│   ├── 📁 frontend
│   ├── 📁 backend
│   ├── ...
│   └── docker-compose.yml
├── Makefile    
├── LICENSE    
└── README.md             
```

## Benchmark Results

| Model        | MedQA | OMSRec |
|--------------|-------:|---------:|
| TransE | xx     | xx       |  xx.x%|  xx.x%  | xx.x%|

More benchmarks are available in the [research paper](https://your-project-website.com/paper).


## Internationalization (i18n)

MedAgent supports English, Chinese, and German languages, implemented using `react-i18next` and `i18next` with dynamic language switching, JSON translation texts, and modularized file structure. To add a new language, update `settings.ts`, create a new language folder, add a translation file, and update the language switcher component.


More information in the [i18n README](frontend/src/i18n/README.md)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Citation

If you use this project in your research, please cite:
```bibtex
@article{mou2025MedAgent,
  author  = {Yongli Mou, Hanbin Chen, Meret Unbehaun, Saif Nasir, Nadine Önelmis, Behrus Puladi and Stefan Decker},
  title   = {MedAgent:  Medical Guidelines Recommendation System Based on Retrieval Augmented Retrieval and Agentic AI Workflows},
  journal = {XXX},
  year    = {202X}
}
```

---
<!-- ---Developed by **Your Name** | [LinkedIn](https://linkedin.com/in/YOURNAME) | [Twitter](https://twitter.com/YOURHANDLE) -->

### Quick Start

We provide a convenient script to start both the frontend and backend services simultaneously:

```bash
# Add execution permission
chmod +x start.sh

# Run the script
./start.sh
```

This script will automatically:
- Check if the necessary dependencies are installed
- Create and activate the conda environment (if it doesn't exist)
- Install the required dependencies
- Start the backend service (http://127.0.0.1:8000)
- Start the frontend service (http://localhost:3000)

You can use `Ctrl+C` to stop all services simultaneously.
