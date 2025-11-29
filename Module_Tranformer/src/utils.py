import numpy as np
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # Sigmoid to get 0-1 probabilities
    probs = 1 / (1 + np.exp(-logits))
    # Threshold 0.5 for binary classification per label
    y_pred = (probs > 0.5).astype(int)
    
    f1_micro = f1_score(labels, y_pred, average='micro')
    f1_macro = f1_score(labels, y_pred, average='macro')
    accuracy = accuracy_score(labels, y_pred)
    
    # ROC AUC handle exception if only one class present in batch
    try:
        roc_auc = roc_auc_score(labels, probs, average='macro')
    except ValueError:
        roc_auc = 0.0
    
    return {
        'f1_micro': f1_micro,
        'f1_macro': f1_macro,
        'roc_auc': roc_auc,
        'accuracy': accuracy
    }