# Toxic Phrase Detection Model

Một model nhận diện các câu nói có chứa từ/cụm từ toxic dựa trên từ điển slang.

## Tính năng

- **Phát hiện từ/cụm từ toxic**: Tự động nhận diện các từ/cụm từ toxic trong câu văn
- **Đếm số lượng**: Đếm chính xác số lượng cụm từ toxic trong mỗi câu
- **Hỗ trợ batch processing**: Xử lý nhiều câu cùng lúc
- **Đánh giá model**: Script đánh giá tự động với các metrics (Precision, Recall, F1-Score)
- **Unit tests**: Bộ test toàn diện đảm bảo chất lượng code

## Cấu trúc dữ liệu

File `slang.csv` chứa các thuộc tính:
- `slang`: Từ/cụm từ slang
- `canonical_form`: Dạng chuẩn của từ
- `type`: Loại (positive, negative, neutral)
- `toxic_score`: Điểm độc hại (1-5)

### Tiêu chí phân loại toxic:
- `type == 'negative'` HOẶC
- `toxic_score >= 3` (ngưỡng mặc định)

## Cài đặt

### Yêu cầu
```bash
pip install pandas
```

### Cấu trúc thư mục
```
.
├── slang.csv                    # Từ điển slang
├── model.py                     # Model phát hiện toxic phrases
├── evaluate_toxic_model.py      # Script đánh giá model
├── test_toxic_model.py          # Unit tests
└── README_TOXIC_MODEL.md        # Tài liệu này
```

## Sử dụng

### 1. Sử dụng trong Python Code

```python
from model import ToxicPhraseDetector

# Khởi tạo detector
detector = ToxicPhraseDetector(
    slang_csv_path='slang.csv',
    toxic_threshold=3
)

# Phát hiện toxic phrases trong một câu
result = detector.detect("This ragebait content is pure brainrot")
print(f"Is Toxic: {result['is_toxic']}")           # True
print(f"Toxic Count: {result['toxic_count']}")     # 2
print(f"Phrases: {result['toxic_phrases']}")       # ['ragebait', 'brainrot']

# Lấy thông tin chi tiết
result_detailed = detector.detect("Stop posting ragebait", return_details=True)
print(result_detailed['details'])
# [{'phrase': 'ragebait', 'position': 14, 'canonical_form': 'ragebait', 
#   'type': 'negative', 'toxic_score': 3}]

# Xử lý nhiều câu
sentences = [
    "This is a nice day",
    "This is pure brainrot",
    "Stop the ragebait and downvoting"
]
results = detector.batch_detect(sentences)
for sentence, result in zip(sentences, results):
    print(f"{sentence}: {result['toxic_count']} toxic phrases")
```

### 2. Sử dụng CLI (Command Line)

#### Phân tích một câu
```bash
python model.py --text "This ragebait is pure brainrot"
```

#### Phân tích file (mỗi dòng một câu)
```bash
python model.py --file sentences.txt --details
```

#### Xem thống kê
```bash
python model.py --stats
```

#### Tùy chỉnh ngưỡng toxic
```bash
python model.py --text "Some text" --threshold 2
```

### 3. Đánh giá Model

Chạy script đánh giá tự động:

```bash
python evaluate_toxic_model.py
```

Script này sẽ:
- Tải model và từ điển toxic phrases
- Chạy test trên các test cases được định nghĩa sẵn
- Tính toán các metrics: Accuracy, Precision, Recall, F1-Score
- Hiển thị kết quả chi tiết cho từng test case
- Lưu kết quả vào file `evaluation_results.json`
- Cung cấp chế độ interactive để test câu tùy ý

Kết quả mẫu:
```
============================================================
TOXIC PHRASE DETECTION MODEL - EVALUATION REPORT
============================================================

Total Test Cases: 30

Confusion Matrix:
  True Positives:  18
  False Positives: 0
  True Negatives:  12
  False Negatives: 0

Performance Metrics:
  Accuracy:        100.00%
  Precision:       100.00%
  Recall:          100.00%
  F1-Score:        100.00%
  Count Accuracy:  100.00%

Phrase Detection:
  Expected Phrases:  30
  Detected Phrases:  30
```

### 4. Chạy Unit Tests

```bash
python test_toxic_model.py
```

Hoặc với unittest:
```bash
python -m unittest test_toxic_model.py -v
```

## API Reference

### ToxicPhraseDetector

#### `__init__(slang_csv_path: str, toxic_threshold: int)`
Khởi tạo detector.

**Tham số:**
- `slang_csv_path`: Đường dẫn đến file slang CSV
- `toxic_threshold`: Ngưỡng toxic_score tối thiểu (mặc định: 3)

#### `detect(sentence: str, return_details: bool = False) -> dict`
Phát hiện toxic phrases trong một câu.

**Input:**
- `sentence`: Câu văn cần phân tích
- `return_details`: Có trả về thông tin chi tiết hay không

**Output:**
```python
{
    'is_toxic': bool,              # Có chứa toxic phrases không
    'toxic_count': int,            # Số lượng toxic phrases
    'toxic_phrases': List[str],    # Danh sách toxic phrases tìm thấy
    'details': List[dict]          # Chi tiết (nếu return_details=True)
}
```

#### `batch_detect(sentences: List[str]) -> List[dict]`
Phát hiện toxic phrases trong nhiều câu.

#### `get_statistics() -> dict`
Lấy thống kê về toxic phrases đã tải.

## Ví dụ Test Cases

```python
# Clean sentences (no toxic)
"This is a wonderful day!"           → is_toxic=False, count=0
"I love programming"                 → is_toxic=False, count=0

# Single toxic phrase
"This is pure brainrot"             → is_toxic=True, count=1
"Stop posting ragebait"             → is_toxic=True, count=1

# Multiple toxic phrases
"This ragebait is brainrot"         → is_toxic=True, count=2
"Downvoted for brainrot ragebait"   → is_toxic=True, count=3

# Case insensitive
"BRAINROT"                          → is_toxic=True, count=1
"BrainRot"                          → is_toxic=True, count=1
```

## Metrics Đánh Giá

Model được đánh giá dựa trên:

1. **Accuracy**: Tỷ lệ phân loại đúng (toxic/non-toxic)
2. **Precision**: Tỷ lệ dự đoán toxic đúng / tổng dự đoán toxic
3. **Recall**: Tỷ lệ phát hiện được toxic / tổng toxic thực tế
4. **F1-Score**: Trung bình điều hòa của Precision và Recall
5. **Count Accuracy**: Tỷ lệ đếm đúng số lượng toxic phrases

## Đặc điểm Kỹ thuật

- **Case-insensitive**: Không phân biệt chữ hoa/thường
- **Word boundaries**: Chỉ khớp từ nguyên vẹn (tránh false positive)
- **Multi-phrase detection**: Phát hiện nhiều cụm từ trong một câu
- **Whitespace normalization**: Xử lý khoảng trắng thừa
- **Unicode support**: Hỗ trợ ký tự Unicode

## Tùy chỉnh

### Thay đổi ngưỡng toxic
```python
# Ngưỡng thấp hơn (phát hiện nhiều hơn)
detector = ToxicPhraseDetector(toxic_threshold=2)

# Ngưỡng cao hơn (chặt chẽ hơn)
detector = ToxicPhraseDetector(toxic_threshold=4)
```

### Thêm test cases mới
Chỉnh sửa function `create_test_cases()` trong `evaluate_toxic_model.py`:

```python
def create_test_cases():
    test_cases = [
        ("Your sentence here", True/False, expected_count),
        # ...
    ]
    return test_cases
```

## Troubleshooting

### Import Error
```bash
# Cài đặt pandas
pip install pandas
```

### File not found
Đảm bảo `slang.csv` nằm cùng thư mục với script hoặc cung cấp đường dẫn đầy đủ:
```python
detector = ToxicPhraseDetector(slang_csv_path='path/to/slang.csv')
```

## License

MIT License

## Tác giả

Developed for toxic phrase detection in social media content.
