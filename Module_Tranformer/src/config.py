# import torch
# import os

# # Device configuration
# DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Paths
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, 'Data', 'train.csv')
# MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'models', 'distilbert_toxic')

# # Model Parameters
# MODEL_NAME = 'distilbert-base-uncased'
# MAX_LEN = 128

# # --- TUNING CHO RTX 3060 6GB ---
# # 1. Giảm Batch Size xuống 8 để an toàn cho VRAM 6GB
# BATCH_SIZE = 8  

# # 2. Tăng số bước tích lũy gradient để mô phỏng batch size lớn hơn
# # (8 batch size * 2 accumulation = tương đương train batch 16)
# GRADIENT_ACCUMULATION_STEPS = 2 

# EPOCHS = 3
# LEARNING_RATE = 2e-5
# FP16 = True # Bật chế độ tính toán 16-bit (quan trọng cho RTX 30xx)

# # Labels
# LABEL_COLS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']


import torch
import os

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'Data', 'train.csv')
MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'models', 'roberta_toxic') 

MODEL_NAME = 'roberta-base' 
MAX_LEN = 128

# Config cho RTX 3060
BATCH_SIZE = 8
GRADIENT_ACCUMULATION_STEPS = 2
EPOCHS = 4 
LEARNING_RATE = 2e-5
FP16 = True

LABEL_COLS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']