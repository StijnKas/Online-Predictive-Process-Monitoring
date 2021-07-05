from collections import defaultdict
from tqdm import tqdm
import itertools

def OPPM(data, configs, label, model, encodings, timefeatures=False, **kwargs):
    """
    The main pipeline function for online predictive process monitoring.

    Parameters:
    - data (river.stream): a river stream object
    - configs (dict): a json file with configs for the given dataset
    - label (labeling): a labeling function from the 'components' folder
    - model (compose.Pipeline): a river pipeline object with a classifier as the last object
    - encodings (FuncTransformer | TransformerUnion): a river FuncTransformer object or, more likely, a TransformerUnion
    - timefeatures (FuncTransformer): optional time feature encoder based on timestamp column from configs
    - params (dict): additional params such as boolean value for feature rollback

    Returns: 
    - preds (dict): a dictionary with predictions throughout each case (probability for positive class)
    - seen (dict): a dictionary with caseid / label pairs for each case 
    - model (compose.Pipeline): the trained model on the whole dataset
    """

    step = iter(model.steps.values())
    for _ in itertools.islice(step, len(model.steps)-1): pass
    model_name = next(step)

    preds, seen, predictors = defaultdict(list), defaultdict(dict), defaultdict(list)
    if 'rollback' in kwargs:
        rollback = kwargs['rollback']
    else: rollback = False
    
    print(f"""Starting the pipeline function. Current parameters:
    Data object: {data.__name__}
    Case ID col: {configs['vartypes']['case_id_col']}
    Activity col: {configs['vartypes']['activity_col']}
    Timestamp col: {configs['vartypes']['timestamp_col']}

    Positive outcome: {label.positive_outcomes} in feature: {label.feature}

    Timefeatures: {True if timefeatures is not False else False}
    Rollback: {rollback}

    Model: {model_name}
    """)
    import time
    time.sleep(0.5) #To print information before tqdm starts

    for x, _ in tqdm(data):
        case_id = x[configs['vartypes']['case_id_col']]
        if case_id not in seen.keys():
            if label.check(x):

                #labeling
                y = label.get(x)

                #if rollback, train model for every version
                if rollback:
                    for version in predictors[case_id]:
                        model.learn_one(version, y)
                
                #else, first get encoded trace, then train model
                else:
                    if timefeatures is not False:
                        time_features = timefeatures.transform_one(x)
                        encoded = encodings.transform_one(x)
                        X = time_features[list(time_features.keys())[0]] | encoded
                    else:
                        X = encodings.transform_one(x)
                
                    model.learn_one(X, y)
                
                #delete encoders from memory
                if timefeatures is not False:
                    del timefeatures.groups[timefeatures._get_key(x)]
                
                for name in encodings.transformers:
                    encoder = encodings[name]
                    del encoder.groups[encoder._get_key(x)]
                
                if rollback: del predictors[case_id]

                #add case id to seen list
                seen.update({case_id:y})
            
            else:

                #encoding
                if timefeatures is not False:
                    time_features = timefeatures.learn_one(x).transform_one(x)
                    encoded = encodings.learn_one(x).transform_one(x)
                    X = time_features[list(time_features.keys())[0]] | encoded
                else:
                    X = encodings.learn_one(x).transform_one(x)

                if rollback:
                    predictors[case_id].append(X)
                
                try:
                    preds[case_id].append(model.predict_proba_one(X)[label.positive_label])
                
                except KeyError:
                    pass

    return(preds, seen, model)