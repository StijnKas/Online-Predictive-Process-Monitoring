import sys
sys.path.append("..")

from river import compose, stats, feature_extraction as fx
from OPPM.river_additions import encoders


def get_encoder(on, by, how):
    """
    Utility function to get river Transformer object from encoder string.
    Since a Transformer object can be seen as a streaming groupby,
    on, by and how are essentially groupby parameters.

    Parameters:
        on (str): The feature on which to encode
        by (str): The feature on which to group
        how (str): The function to use with the encoder

    Returns:
        transformer (compose.FuncTransformer): The River transformer object
    """

    if how == "agg_mean":    
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=stats.Mean()))

    if how == "agg_mode":
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=stats.Mode()))

    if how == "agg_max":        
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=stats.Max()))

    if how == "agg_min":        
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=stats.Min()))

    if how == "count":
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=stats.Count()))

    if how == "agg_nunique":
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=encoders.CountUnique()))

    if how == "laststate":
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=encoders.Last()))

    if how == "firststate":
        return compose.FuncTransformer(fx.Agg(on=on, by=by, how=encoders.First()))
    
    if how == "agg_std":
        pass

    if how == "index":
        pass

    print("Unknown aggregation function: ", how)
    pass

def OTFE(encodelist, by='Case ID'): 
    """
    'On the fly encoding': define the TransformerUnion which performs encoding.
    
    Parameters: 
        encodelist (pd.DataFrame): Encoder list from get_encoder_list()

    Returns: 
        agg (river.TransformerUnion): TransformerUnion object with all required encoders
    """

    agg = compose.TransformerUnion()
    templist = encodelist[encodelist == 1].stack().index.tolist()
    for pair in templist:
        varname = encodelist["Variable"][pair[0]]
        try:
            agg += get_encoder(varname, by, pair[1]).func
        except AttributeError:
            print(f"Unknown pair: {pair}")
    return agg


def _get_encoder_list(excelname):
    """
    Convenience function for reading the excel name and renaming columns.

    Parameters:
        excelname (str): Filepath and name of the encoder list

    Returns:
        output (pd.DataFrame): A dataframe with the encoder pairs
    """
    import pandas as pd
    output = pd.read_excel(excelname)
    output = output.rename(columns={output.columns[0]: "Variable"})
    return output

def get_encoder_list(dataset, filepath = "OPPM/datasets/encoders"):
    """
    Utility function for either finding or generating the encoder list matrix.
    Note: as of right now, generate_template() is not included.
    This would otherwise create a matrix with all available encoders vs variables.

    Parameters:
        dataset (str): The name of the dataset
        filepath (str): The directory of the dataset
    
    Returns:
        encodelist (pd.DataFrame): Dataframe matrix of encoders vs variables
    """

    from os import path
    excelname = f"{filepath}/{dataset}.xls"
    if path.exists(excelname):
        encodelist = _get_encoder_list(excelname)
        return encodelist
    else: 
        #generate_template(vartypes, encoder_list).to_excel(excelname)
        print(f"Filename {excelname} does not exsist.")
        return None