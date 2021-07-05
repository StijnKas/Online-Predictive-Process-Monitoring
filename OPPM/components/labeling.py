class labeler():
    """
    Base labeling function: current implementation is value-occurence
    Initiate by setting various values, call to check or get label
    """

    def __init__(self, outcomes:set, positive_outcomes:set, feature:str, positive_label=1, negative_label=0):
        """
        Initiate labeling function

        Parameters:
            outcomes (set): The set of outcomes to represent a label
            positive_outcomes (set): The outcomes to return a 'positive' label
            feature (str): The feature to look for the set of outcomes
            positive_label (str): The label to return as positive label
            negative_label (str): The label to return as negative label
        """
        
        self.outcomes = outcomes
        self.positive_outcomes = positive_outcomes
        self.feature = feature
        self.positive_label = positive_label
        self.negative_label = negative_label

    def check(self, x):
        """
        Quick set comprehension check if feature is in outcomes
        """

        if x[self.feature] in self.outcomes:
            return True
        else:
            return False
    
    def get(self, x):
        """
        Retrieve the actual label
        """
        return self.positive_label if x[self.feature] in self.positive_outcomes else self.negative_label
    
    def check_get(self, x):
        """
        Set comprehension to see if feature in outcomes:
        - If feature is in outcomes, return outcome
        - Otherwise, return None
        """
        if x[self.feature] in self.outcomes:
            return self.positive_label if x[self.feature] in self.positive_outcomes else self.negative_label
        else:
            return None

