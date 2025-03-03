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

### Key components and terms
- **Large Language Models (LLMs)**: At the core of the system, LLMs such as GPT-based models are utilized to understand medical queries and generate responses in natural language, ensuring that recommendations are presented in an intuitive, easy-to-understand format for doctors.

- **Agentic AI Workflow**: This component enables the system to perform complex tasks autonomously. It orchestrates the interaction between different models and databases, ensuring a smooth process for retrieving relevant medical guidelines, processing them, and providing actionable insights. The agentic behavior allows the system to adapt to different contexts based on user input and system status.

- **RAG Pipeline**: The system integrates the Retrieve-and-Generate (RAG) pipeline, which enables it to query relevant databases for up-to-date medical information. This includes using retrieval-based techniques to extract the most relevant data from external sources (e.g., medical research, guidelines databases) and then generating personalized recommendations or explanations for the doctor.

### Role-based interactions

The system is designed to serve two primary user roles:

- **Doctors (End-users)**: They interact with the system to receive medical recommendations, guidelines, and insights based on patient data and clinical queries.

- **Knowledge Maintainers (Developers)**: These users are responsible for developing / adjusting the system in two ways:
  - Update the system's knowledge base (ensure medical guidelines are updated, so medical knowledge is up-to-date)
  - Update the system's workflows (integrate also new AI models, test new workflows, regularly improve and handle emerging technical trends and innovations)

To ensure that end-users cannot change established systems AND are not confused / overwhelmed by technical details, these users will not see all interaction possibilities, but instead have only access to the chatbot and overview over the system's knowledge base

## Components


- Frontend [Next.js](https://nextjs.org/docs): The user interface is built with Next.js, providing a modern, responsive, and fast application where doctors can input queries, review recommendations, and interact with the AI-powered assistant. The frontend communicates with the backend (Flask) to handle the logic and AI operations.

- Backend [Flask](https://flask.palletsprojects.com/en/stable/): The backend is built with Flask, handling API requests, interacting with databases, running AI models, and serving the AI-generated guidelines and recommendations to the frontend.
- Databases:
  - Postgres is used to store and manage structured medical data.
  - Neo4j (Graph Database) is used for knowledge representation, allowing the system to model medical relationships, such as drug interactions or disease pathways.
  - Vector Database (e.g., FAISS or similar) is employed to store and query embeddings of medical guidelines and knowledge for efficient retrieval.

- Authentication & Security: The system uses Keycloak for secure authentication and user management. This ensures that only authorized personnel (e.g., doctors and developers) can access the system and modify sensitive data.



## Installation
To keep installation easy and independent of the concrete machine executing it, docker will be used to handle start up and also installation.

### Docker-compose
Execute `docker/docker-compose.yml` as you would execute any docker-compose file.
- See e.g., [this documentation](https://www.geeksforgeeks.org/docker-compose/) for aid


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
The system will be tested on a custom validation setup on a dataset specifically designed to assess performance on questions answered using the guidelines from the oral and maxillofacial surgery specialty.

**! TODO: display for performance**

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
