import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
# from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, TrainingArguments
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification, TrainingArguments

# Imports from our src package
from src import config
from src.preprocessing import clean_text_bert
from src.dataset import ToxicDataset
from src.train import MultiLabelTrainer
from src.utils import compute_metrics

def main():
    print(f"Starting Training Pipeline on {config.DEVICE}")
    
    # 1. Load Data
    print("Loading data...")
    if not os.path.exists(config.DATA_PATH):
        raise FileNotFoundError(f"Data not found at {config.DATA_PATH}")
        
    df = pd.read_csv(config.DATA_PATH)
    # Uncomment next line for quick testing
    # df = df.sample(5000).reset_index(drop=True)
    
    # 2. Preprocess
    print("Preprocessing texts...")
    df['cleaned_text'] = df['comment_text'].apply(clean_text_bert)
    
    # 3. Split
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['cleaned_text'].values, 
        df[config.LABEL_COLS].values, 
        test_size=0.15, 
        random_state=42
    )
    
    # 4. Compute Weights for Imbalance
    print("Computing class weights...")
    num_positives = np.sum(train_labels, axis=0)
    # Avoid division by zero
    num_positives = np.clip(num_positives, 1, None) 
    class_weights = (len(train_labels) - num_positives) / num_positives
    # class_weights = np.clip(class_weights, 1.0, 20.0)
    class_weights = np.clip(class_weights, 1.0, 8.0)
    print(f"Class Weights: {class_weights}")

    # 5. Tokenizer & Datasets
    tokenizer = RobertaTokenizerFast.from_pretrained(config.MODEL_NAME)
    train_dataset = ToxicDataset(train_texts, train_labels, tokenizer, config.MAX_LEN)
    val_dataset = ToxicDataset(val_texts, val_labels, tokenizer, config.MAX_LEN)

    # 6. Model
    model = RobertaForSequenceClassification.from_pretrained(
        config.MODEL_NAME, 
        num_labels=len(config.LABEL_COLS),
        problem_type="multi_label_classification"
    )
    model.to(config.DEVICE)

    # 7. Trainer Setup
    training_args = TrainingArguments(
        output_dir='./results_roberta',
        num_train_epochs=config.EPOCHS,
        
        per_device_train_batch_size=config.BATCH_SIZE,
        per_device_eval_batch_size=config.BATCH_SIZE,
        gradient_accumulation_steps=config.GRADIENT_ACCUMULATION_STEPS,
        
        fp16=config.FP16, 
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=50,
        eval_strategy="epoch", 
        save_strategy="epoch",
        save_total_limit=1,
        learning_rate=config.LEARNING_RATE,
        
        dataloader_num_workers=0, 
        report_to="none"
    )

    trainer = MultiLabelTrainer(
        class_weights=class_weights,
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    # 8. Train
    print("Training started...")
    trainer.train()

    # 9. Evaluate & Save
    print("Evaluating...")
    results = trainer.evaluate()
    print(f"Results: {results}")

    print(f"Saving model to {config.MODEL_SAVE_PATH}")
    model.save_pretrained(config.MODEL_SAVE_PATH)
    tokenizer.save_pretrained(config.MODEL_SAVE_PATH)
    print("Pipeline Complete!")

if __name__ == "__main__":
    main()