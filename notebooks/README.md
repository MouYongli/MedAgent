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

| Notebook                                       | Purpose                                                                                                                                                                          |  Integrated in Frontend?   |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------:|
| [`1_guideline.ipynb`](./nbs/1_guideline.ipynb) | Tests loading and parsing AWMF guideline structure; includes visual inspection and analysis of document types. Only needs execution once, then guidelines are properly inserted. |             ✗              |


## How to Run
You can run the notebooks inside a Docker container using the provided Conda environment:

0. Ensure the docker compose from the main project is running. We require access to both the MongoDB this starts AND the Backend API.

1. Build the container:
   ```bash
   cd docker
   docker build -t jupyter-medagent .
   ```

2. Run it
   ```bash
   docker run -d -p 8888:8888 -v ${PWD}/../:/workspace --name jupyter-medagent-container jupyter-medagent
   ``` 

3. Access notebooks under http://localhost:8888/lab/workspaces/auto-L/tree/nbs/1_guideline.ipynb


## Transform to frontend
TODO
