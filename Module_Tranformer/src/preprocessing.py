import re

# 1. Obfuscation Patterns
PROFANITY_PATTERNS = [
    (r'f[\W_]*u[\W_]*c[\W_]*k', 'fuck'),
    (r'sh[\W_]*i[\W_]*t', 'shit'),
    (r'b[\W_]*i[\W_]*t[\W_]*c[\W_]*h', 'bitch'),
    (r'a[\W_]*s[\W_]*s[\W_]*h?[\W_]*o?[\W_]*l[\W_]*e?', 'asshole'),
    (r'd[\W_]*a[\W_]*m[\W_]*n', 'damn'),
    (r'idi0t', 'idiot'),
    (r'h0le', 'hole'),
]

# 2. Slang Map
SLANG_MAP = {
    r'\bkys\b': 'kill yourself',
    r'\bstfu\b': 'shut the fuck up',
    r'\bgtfo\b': 'get the fuck out',
    r'\bu\b': 'you',
    r'\bur\b': 'your',
    r'\br\b': 'are',
}

# 3. Positive Context Patterns
POSITIVE_ADJECTIVES = [
    "amazing", "awesome", "brilliant", "excellent", "fantastic", 
    "good", "great", "incredible", "love", "lovely", "magnificent", 
    "nice", "perfect", "spectacular", "superb", "wonderful", "beautiful",
    "best", "better", "genius", "talented", "smart", "funny", "cool"
]
positive_pattern = "|".join(POSITIVE_ADJECTIVES)
CONTEXT_PATTERN = re.compile(
    rf"\b(fucking|fuckin|damn|bloody)\s+({positive_pattern})\b",
    flags=re.IGNORECASE
)

def clean_text_bert(text):
    if not isinstance(text, str):
        return ""
        
    text = text.lower()
    
    # --- MỚI: Xử lý ngữ cảnh đặc biệt "Killer" ---
    # Nếu "killer" đi với "at/in/on/with" -> thường là khen (giỏi về cái gì đó)
    # killer at chess -> expert at chess
    text = re.sub(r'\bkiller\s+(at|in|on|with)\b', r'expert \1', text)
    
    # Nếu "killer" đi với các từ tích cực (killer app, killer feature, killer move)
    text = re.sub(r'\bkiller\s+(app|feature|move|shot|deal)\b', r'great \1', text)
    # ---------------------------------------------

    # 1. Normalize obfuscated profanity
    for pattern, repl in PROFANITY_PATTERNS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    
    # 2. Normalize Slang
    for pattern, repl in SLANG_MAP.items():
        text = re.sub(pattern, repl, text)

    # 3. Handle Positive Context (fucking amazing -> very amazing)
    text = CONTEXT_PATTERN.sub(lambda m: f"very {m.group(2)}", text)

    # 4. Normalize leet speak & chars
    text = re.sub(r'@', 'a', text)
    text = re.sub(r'\$', 's', text)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text) # coool -> cool
    
    # 5. Cleanup
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text