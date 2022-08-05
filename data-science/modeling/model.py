
class Model():
    
    def init_model(self, model_type = None, params:dict = {}):
        return model_type(**params)
        
    def train(self, model, features, labels): 
        return model.fit(features, labels)
    
    def score(self, model, features, true_labels):
        preds = model.predict(features)
        return {
          "accuracy": sum(true_labels==preds)/len(true_labels)
        }
