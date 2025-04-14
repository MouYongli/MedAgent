# Notebooks

The purpose of the listed [Jupyter Notebooks](https://jupyter.org/install) is to:
- Rapidly prototype and prepare studies required for the project.
- Suggest and experiment with visualizations for the evaluation.
- Interact with data directly (currently via MongoDB), before fully integrating with the backend.

Access to the [MongoDB](https://www.mongodb.com/try/download/community) is **currently NOT done via backend calls**. This will be refactored step by step.
- A separate document collection is used for these experiments to avoid interfering with the main system with the name `nb_document_store`


What you'll find in this README
- Overview of the current notebooks and their purpose.
- How to execute the notebooks.
- TODOs for translating notebook logic into the production system (e.g., the frontend).

---

## Contained Notebooks

| Notebook | Purpose | Integrated in Frontend? |
|----------|---------|--------------------------|
| [`1_guideline.ipynb`](./nbs/1_guideline.ipynb) | _TODO: fill in_ | ✗ |


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

3. Access notebooks under http://localhost:8888/lab/tree/nbs


## Transform to frontend
TODO
