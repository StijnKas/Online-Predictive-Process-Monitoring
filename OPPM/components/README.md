# Components
This folder contains four custom components: encoding, labeling, pipeline and tools.

encoding.py contains the functions needed to generate and order the encoders. The encoders themselves are found in river_additions and are called from the function in this file.

labeling.py contains the value-occurence based labeling function. If more labeling functions were to be created they would be found here.

pipeline.py contains the main pipeline function which combines all other components and iterates through the dataset. 

tools.py contains utility functions to support river operations.