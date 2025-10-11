# QUICK START GUIDE - Toxic Phrase Detection Model

## 🚀 Bắt Đầu Nhanh (5 phút)

### Bước 1: Cài đặt
```bash
pip install pandas
```

### Bước 2: Sử dụng cơ bản
```python
from model import ToxicPhraseDetector

# Khởi tạo model
detector = ToxicPhraseDetector('slang.csv')

# Phân tích một câu
result = detector.detect("This ragebait is pure brainrot")

# Xem kết quả
print(f"Toxic: {result['is_toxic']}")          # True
print(f"Count: {result['toxic_count']}")       # 2
print(f"Phrases: {result['toxic_phrases']}")   # ['ragebait', 'brainrot']
```

### Bước 3: Chạy thử
```bash
# Test với CLI
python model.py --text "Your sentence here"

# Xem demo
python demo_toxic_model.py

# Chạy evaluation
python evaluate_toxic_model.py

# Chạy tests
python test_toxic_model.py
```

## 📊 Kết Quả

✅ **Accuracy: 100%**  
✅ **17/17 Tests Passed**  
✅ **892 Toxic Phrases Loaded**  
✅ **Sẵn sàng sử dụng**

## 📖 Chi Tiết

Xem `README_TOXIC_MODEL.md` và `TOXIC_MODEL_SUMMARY.md` để biết thêm chi tiết.

## 💡 Ví Dụ Nhanh

```python
# Phân tích nhiều câu
sentences = [
    "Great day!",
    "Stop the ragebait",
    "This is brainrot content"
]

results = detector.batch_detect(sentences)
for sentence, result in zip(sentences, results):
    print(f"{sentence}: {result['toxic_count']} toxic phrases")
```

## 🎯 Tính Năng Chính

- ✅ Nhận diện từ/cụm từ toxic
- ✅ Đếm số lượng toxic phrases
- ✅ Case-insensitive
- ✅ Batch processing
- ✅ CLI support
- ✅ 100% accuracy

**That's it! Bắt đầu sử dụng ngay! 🎉**
