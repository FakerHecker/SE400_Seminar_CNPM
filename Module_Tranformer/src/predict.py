import torch
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
from src.config import MODEL_SAVE_PATH, MODEL_NAME, MAX_LEN, DEVICE, LABEL_COLS
from src.preprocessing import clean_text_bert

class ToxicPredictor:
    def __init__(self, model_path=None):
        self.device = DEVICE
        path = model_path if model_path else MODEL_SAVE_PATH
        print(f"Loading model from {path}...")
        
        try:
            self.tokenizer = RobertaTokenizerFast.from_pretrained(path)
            self.model = RobertaForSequenceClassification.from_pretrained(path).to(self.device)
            self.model.eval()
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Using default tokenizer for fallback/testing setup...")
            self.tokenizer = RobertaTokenizerFast.from_pretrained(MODEL_NAME)
            self.model = None

    def predict(self, text):
        if self.model is None:
            return {"error": "Model not loaded"}

        cleaned_text = clean_text_bert(text)
        
        encoding = self.tokenizer.encode_plus(
            cleaned_text,
            add_special_tokens=True,
            max_length=MAX_LEN,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probs = torch.sigmoid(logits).cpu().numpy()[0]

        result = {
            "text": text,
            "cleaned_text": cleaned_text,
            "predictions": {},
            "status": "CLEAN",
            "color": "clean"
        }
        
        harmful_labels = ['toxic', 'severe_toxic', 'threat', 'insult', 'identity_hate']
        is_harmful = False
        is_obscene = False
        threshold = 0.5

        for idx, label in enumerate(LABEL_COLS):
            score = float(probs[idx])
            result["predictions"][label] = score
            
            if score > threshold:
                if label in harmful_labels:
                    is_harmful = True
                if label == 'obscene':
                    is_obscene = True

        if is_harmful:
            result["status"] = "TOXIC CONTENT DETECTED"
            result["color"] = "toxic"
        elif is_obscene:
            result["status"] = "PROFANITY DETECTED (SAFE CONTEXT)"
            result["color"] = "obscene"
        else:
            result["status"] = "CLEAN CONTENT"
            result["color"] = "clean"
                
        return result