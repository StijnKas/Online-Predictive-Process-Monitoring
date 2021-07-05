from river.stats import base
from datetime import datetime, timedelta
from collections import defaultdict

class Last(base.Univariate):
    """
    Last value encoder.

    Parameters:
        last_value (str): The last (non-na) value in the group.
    
    """

    def __init__(self):
        self.last_value = None
    
    def update(self, x=None):
        if x != "" and x != None:
            self.last_value = x
        return self
    
    def get(self):
        return self.last_value

    

class First(base.Univariate):
    """
    First value encoder.

    Parameters: 
        first_value (str): The first value in the group.
    
    """

    def __init__(self):
        self.first_value = None
    
    def update(self, x=None):
        if self.first_value == None and x != "" and x != None: 
            self.first_value = x
        return self

    def get(self):
        return self.first_value

class CountUnique(base.Univariate):
    """
    A simple counter for unique values.

    Parameters:
        n (int): The current number of unique observations.
    
    """

    def __init__(self):
        self.n = 0
        self.prev_values = set()
    
    def update(self, x=None):
        if x not in self.prev_values:
            self.prev_values.add(x)
            self.n += 1
        return(self)
    
    def get(self):
        return(self.n)

class Index(base.Univariate):
    """
    A simple function to encode a dict for every value for each index.

    Parameters:
        features (dict): For each index, the corresponding value.
        featurename (str): The name of the feature to encode
        i (int): The current index within the case

    """

    def __init__(self, columnname='feature'):
        self.i = 0
        self.features = dict()
        self.featurename = columnname
    
    def update(self, x=None):
        self.features[str(f'{self.featurename}_{self.i}')] = x
        self.i += 1
        return(self)
    
    def get(self):
        return(self.features)

class TimeFeatures(base.Univariate):
    """
    A complex encoder returning various features based on a timestamp

    Parameters:
        x (datetime.datetime): The timestamp to encode

    Returns:
        features (dict): The various features encoded as dict
    """

    def __init__(self):
        self.features = defaultdict(list)
        self._first = 0
        self._previous = 0

    def update(self, x):
        if self._first == 0: self._first = x
        self.features = {
            'month': int(x.strftime("%m")),
            'weekday': int(x.strftime("%u")),
            'hour': int(x.strftime("%H")),
            'timesincemidnight': int((x - datetime.combine(x.date(),datetime.min.time())).total_seconds()),
            'timesincecasestart': int((x - self._first).total_seconds()),
            'timesincelastevent': int((x - self._previous).total_seconds() if self._previous != 0 else 0)#,
        }
        self._previous = x
        return self

    def get(self):
        return self.features
