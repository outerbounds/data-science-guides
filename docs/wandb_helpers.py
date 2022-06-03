import os
import wandb
def plot_results(X_train, y_train, X_test, y_test, 
                 y_pred, y_probs, clf, labels):
    wandb.init(entity=os.getenv("WANDB_ENTITY"), 
               project=os.getenv("WANDB_PROJECT"), 
               mode="offline")
    wandb.sklearn.plot_class_proportions(y_train,
                                         y_test, 
                                         labels)
    wandb.sklearn.plot_learning_curve(clf, 
                                      X_train, 
                                      y_train)
    wandb.sklearn.plot_roc(y_test, y_probs, labels)
    wandb.sklearn.plot_precision_recall(y_test, 
                                        y_probs, 
                                        labels)
    wandb.sklearn.plot_feature_importances(clf)
    wandb.sklearn.plot_classifier(
        clf, X_train, X_test, y_train, y_test, y_pred, 
        y_probs, labels, is_binary=True, 
        model_name='RandomForest'
    )
    wandb.finish()
