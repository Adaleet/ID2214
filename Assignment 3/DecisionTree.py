from DecisionTree import DecisionTree
import numpy as np
from collections import Counter

class RandomForest(): 
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=2, n_feature=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_feature
        self.trees = [] 
        
    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees): 
            tree = DecisionTree(max_depth = self.max_depth,
                         min_samples_split = self.min_samples_split,
                         n_features=self.n_features)
            X_sample, y_sample = self._bootstrap_samples(X, y)
            tree.fit(X_sample, y_sample) 
            
    def _bootstrap_samples(self, X, y):
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def __most_common_label(self, y): 
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common # Returning the most common occurence of tuples. 
    
     
    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(predictions, 0, 1)
        #[[1, 0, 1, 1], [0, 0, 1, 1], [] ] // First prediction contains inner list of predictions
        # Instead of this, we want to save the predictions of each sample after different X given deicsion trees, 
        # , for each sample to be given in the same list, i.e. First list = results of different decision trees for the first sample. 
        # etc. for each different list.
        
        predictions = np.array([self._most_common_label(pred) for pred in tree_preds])
        return predictions