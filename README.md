# Online Predictive Process Monitoring
An online Predictive Process Monitoring approach using [River](https://github.com/online-ml/river). 

Part of the Streaming Analytics 4 Process Mining track at ICPM 2021: https://sa4pm.win.tue.nl/2021/wp-content/uploads/sites/3/2021/10/ICPM2021-paper_170_2.pdf. 

## Directory
- *OPPM* contains the source functions and datasets for the pipeline
- *examples.ipynb* demonstrates the use of encoders, labeling & rollback
- *paper_results.ipynb* lists the performed experiments for the paper

## Docker
The approach was created in Docker for compatibility, using Visual Studio Code's Dev Container functionality. It has not been tested in a different IDE or outside of Docker. The Dockerfile and requirements.txt should allow for an easy compilation of the entire project directory. For reference, the following VSCode extensions were installed: ["ms-python.python", "ms-toolsai.jupyter", "ms-azuretools.vscode-docker"]
