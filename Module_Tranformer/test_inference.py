from ..src.predict import ToxicPredictor

predictor = ToxicPredictor()

test_cases = [
    "You're a killer at playing chess!",       # Case đang lỗi
    "This is a killer app.",                   # Case slang khác
    "He is a serial killer.",                  # Case toxic thật (không có 'at')
    "I will kill you.",                        # Case threat
    "This is fucking amazing"                  # Case context cũ
]

print("-" * 50)
for text in test_cases:
    result = predictor.predict(text)
    print(f"Input:    {text}")
    print(f"Cleaned:  {result['cleaned_text']}") 
    print(f"Is Toxic: {result['is_toxic']}")
    if result['is_toxic']:
         # In ra label toxic cụ thể
         print("Labels:", {k:v for k,v in result['predictions'].items() if v > 0.5})
    print("-" * 50)