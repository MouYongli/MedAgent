FROM continuumio/miniconda3

COPY environment.yml /tmp/environment.yml

RUN conda install -n base -c conda-forge mamba
RUN mamba env create -f /tmp/environment.yml
SHELL ["conda", "run", "-n", "manual-medagent", "/bin/bash", "-c"]
WORKDIR /workspace

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager || true
EXPOSE 8888
CMD ["conda", "run", "-n", "manual-medagent", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
