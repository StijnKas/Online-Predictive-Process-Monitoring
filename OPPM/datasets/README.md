# Datasets
For storage reasons, the datasets themselves are not stored in GitHub, though they can be manually inserted into this folder. In the /encoders directory, the various encoder configurations for different datasets can be found. In the configs.json file, settings for various datasets can be given by the same format: 

- "vartypes" denotes the different types of variables in the dataset, expecting at least the case id column, activity column and timestamp column for the activity.
- "params" denotes the parameters for real-time converting of variables in a river stream function, such as the type conversions and the timestamp conversions.