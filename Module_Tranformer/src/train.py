import torch
import torch.nn as nn
from transformers import Trainer
from src.config import DEVICE

class MultiLabelTrainer(Trainer):
    """
    Custom Trainer to handle Class Imbalance using Weighted Loss
    """
    def __init__(self, class_weights, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Move weights to device
        self.class_weights = torch.tensor(class_weights, dtype=torch.float).to(DEVICE)

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        
        # Weighted BCEWithLogitsLoss
        loss_fct = nn.BCEWithLogitsLoss(pos_weight=self.class_weights)
        loss = loss_fct(logits, labels)
        
        return (loss, outputs) if return_outputs else loss