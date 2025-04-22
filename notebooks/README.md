# Notebooks

The purpose of the listed [Jupyter Notebooks](https://jupyter.org/install) is to:
- Rapidly prototype and prepare studies required for the project.
- Suggest and experiment with visualizations for evaluation metrics.
- Interact with data directly (currently via MongoDB), before full backend integration.

Access to the [MongoDB](https://www.mongodb.com/try/download/community) is **currently NOT done via backend calls**. This will be refactored step by step.
- To prevent conflicts with the main system data, a separate document collection is used: `nb_document_store`

## What you'll find in this README

- Overview of current notebooks and their purpose
- Instructions to run notebooks using Docker
- TODOs for transforming notebook logic into frontend/backend components

---

## Contained Notebooks

| Notebook                                                       | Purpose                                                                                                                                           | Integrated in Frontend? |
|:---------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------:|
| [`1_guideline.ipynb`](./nbs/1_guideline.ipynb)                 | Tests loading and parsing AWMF guideline structure; includes visual inspection and analysis of document types. Only needs execution once.         |            ✗            |
| [`2_question_dataset.ipynb`](./nbs/2_question_dataset.ipynb)   | Interactively inspects and manipulates question classification and guideline linkage, exploring how structured datasets map to document coverage. |            ✗            |
| [`3_simple_generation.ipynb`](./nbs/3_simple_generation.ipynb) | Prototypes a basic guideline-to-answer pipeline using the backend generator (e.g., LLM); used to test prompt engineering and model behavior.      |            ✗            |

## How to Run
You can run the notebooks inside a Docker container using the provided Conda environment:

0. Ensure the docker compose from the main project is running. We require access to both the MongoDB this starts AND the Backend API. Also, assure that you copied the template `.env`, renamed to `.local-env` and fill out the required properties to setup the workflows.

1. Build the container:
   ```bash
   cd docker
   docker build -t jupyter-medagent .
   ```

2. Run it
   ```bash
   docker run -d -p 8888:8888  --env-file ../.local-env -v ${PWD}/../:/workspace --name jupyter-medagent-container jupyter-medagent
   ``` 

3. Access notebooks under http://localhost:8888/lab/workspaces/auto-L/tree/nbs/1_guideline.ipynb


## Transform to frontend
TODO
