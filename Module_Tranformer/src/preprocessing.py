import re

# 1. PROFANITY PATTERNS – BẮT BIẾN THỂ / OBFUSCATED PROFANITY
# Giữ lại danh sách này vì nó giúp Tokenizer hiểu từ gốc
PROFANITY_PATTERNS = [
    (r'f[\W_]*u[\W_]*c[\W_]*k+', 'fuck'),
    (r'f[\W_]*u[\W_]*k+', 'fuck'),
    (r'f[\W_]*u[\W_]*q+', 'fuck'),
    (r'f[\W_]*v[\W_]*c[\W_]*k+', 'fuck'),
    (r'f[\W_]*u[\W_]*x+', 'fuck'),
    (r"f[\W_]*u[\W_]*c?[\W_]*k[\W_]*in[g']?", "fucking"),
    (r's[\W_]*h[\W_]*i[\W_]*t+', 'shit'),
    (r's[\W_]*h[\W_]*1[\W_]*t+', 'shit'),
    (r's[\W_]*h[\W_]*\*[\W_]*t', 'shit'),
    (r'b[\W_]*i[\W_]*t[\W_]*c[\W_]*h+', 'bitch'),
    (r'b[\W_]*1[\W_]*t[\W_]*c[\W_]*h+', 'bitch'),
    (r'a[\W_]*s[\W_]*s+', 'ass'),
    (r'a[\W_]*s[\W_]*s[\W_]*h?[\W_]*o?[\W_]*l[\W_]*e?', 'asshole'),
    (r'd[\W_]*a[\W_]*m[\W_]*n', 'damn'),
    (r'i[\W_]*d[\W_]*i[\W_]*o[\W_]*t+', 'idiot'),
    (r'1[\W_]*d[\W_]*i[\W_]*0[\W_]*t+', 'idiot'),
    (r'd[\W_]*i[\W_]*c[\W_]*k+', 'dick'),
    (r'p[\W_]*u[\W_]*s[\W_]*s[\W_]*y+', 'pussy'),
    (r's[\W_]*l[\W_]*u[\W_]*t+', 'slut'),
    (r'w[\W_]*h[\W_]*o[\W_]*r[\W_]*e+', 'whore'),
]

# 2. LEET NORMALIZATION
LEET_MAP = {
    '@': 'a', '$': 's', '0': 'o', '1': 'i', '!': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't'
}

def normalize_leet(text):
    for k, v in LEET_MAP.items():
        text = text.replace(k, v)
    return text

def reduce_repetition(text):
    # cooool -> cool
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def clean_text_bert(text):
    """
    Standard Cleaning for RoBERTa.
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()

    # Normalize leet: h3ll -> hell
    text = normalize_leet(text)

    # Replace obfuscated profanity
    for pattern, repl in PROFANITY_PATTERNS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # Reduce repeated characters
    text = reduce_repetition(text)

    # Remove URLs, IPs (Thay bằng khoảng trắng)
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', ' ', text)

    # Chuẩn hóa khoảng trắng (Quan trọng: Không xóa dấu câu)
    text = re.sub(r'\s+', ' ', text).strip()

    return text