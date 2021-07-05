import sys
sys.path.append("..")
from OPPM.river_additions.converters import *

def to_params(configs:dict):
    """
    Change all converter strings to their functions 

    Parameters:
        configs (dict): Dict with dataset settings
    
    Returns:
        configs (dict): Dict with dataset settings where strings were converted to functions
    """

    for variable, converter in configs['params']['converters'].items():
        configs['params']['converters'][variable] = eval(converter)
    return(configs)

def reset(dataset, directory, encodelist):
    """
    Convenience function to reset river data object, configs and encoders
    Useful for running multiple experiments or comparing different datasets

    Parameters:
        dataset (str): Name of the dataset
        directory (str): Location of the dataset
        encodelist (str): Name of the encode list
    
    Returns: 
        data (compose.Stream): River stream dataset iterable object at row 0
        configs (dict): The dataset configurations
        timefeatures (FuncTransformer): River object of the time-based features
        encodings (TransformerUnion): River object of the encodings
    """

    from river import stream
    from river import feature_extraction as fx
    from OPPM.river_additions import encoders
    from OPPM.components import encoding

    configs = data_set(dataset, directory)
    data = stream.iter_csv(f"{directory}/{dataset}.csv", **configs['params'])
    timefeatures = fx.Agg(
        on=configs['vartypes']['timestamp_col'],
        by=configs['vartypes']['case_id_col'],
        how=encoders.TimeFeatures()
    )
    encodings = encoding.OTFE(encoding.get_encoder_list(encodelist), by=configs['vartypes']['case_id_col'])

    return(data, configs, timefeatures, encodings)

def xes_to_csv(filepath, filename):
    """
    Utility function to convert xes event logs to csv files
    """

    try:
        import pm4py
    except:
        #Not in requirements.txt as it's quite large and only used here
        print('Please manually import pm4py using "pip install pm4py"')
    
    log = pm4py.read_xes(f"{filepath}/{filename}.xes")
    df = pm4py.convert_to_dataframe(log)
    df.to_csv(f"{filepath}/{filename}.csv", 
              index=False,
              date_format= "%Y-%m-%d %H:%M:%S")

def data_set(dataset, directory):
    """
    Convenience function to either import csv or convert xes; import configs
    """

    import json
    from os import path

    if not path.exists(f"{directory}/{dataset}.csv"):
        print(f"No CSV file {dataset} exists in {directory}.")
        print("Checking for XES file")
        if path.exists(f"{directory}/{dataset}.xes"):
            print("Converting XES to CSV")
            try: 
                xes_to_csv(directory, dataset)
            except:
                print("Failed when trying to convert XES to CSV")

    with open(f"{directory}/configs.json", "r") as f:
        try: 
            configs = json.loads(f.read())[dataset]
        except:
            print(f"Check if there is a json file in the directory with configs for the given dataset {dataset}.")
    
    return(to_params(configs))

