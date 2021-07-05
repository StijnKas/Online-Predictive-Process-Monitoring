# Online Predictive Process Monitoring
An online Predictive Process Monitoring approach using [River](https://github.com/online-ml/river).

## Directory
- *OPPM* contains the source functions and datasets for the pipeline
- *examples.ipynb* demonstrates the use of encoders, labeling & rollback
- *paper_results.ipynb* lists the performed experiments for the paper

## Docker
The approach was created in Docker for compatibility, using Visual Studio Code's Dev Container functionality. It has not been tested in a different IDE or outside of Docker. The Dockerfile and requirements.txt should allow for an easy compilation of the entire project directory. For reference, the following VSCode extensions were installed: ["ms-python.python", "ms-toolsai.jupyter", "ms-azuretools.vscode-docker"]