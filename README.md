## Hướng dẫn chạy Module AI

### Bước 0: Clone Project

### Bước 1: Chuyển về thư mục: module/tranformer

### Bước 2: Cài đặt Dependencies

```bash
# Cài đặt môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo:
.\venv\Scripts\Activate

# Cài đặt các packages cần thiết
pip install -r requirements.txt
```
*Lưu ý: Nếu muốn chạy luôn thì cài đặt thêm model nằm ở đây: https://drive.google.com/file/d/1mr5KgYs_VOVmBdN-nEr4wZjaktWv2KLt/view?usp=sharing*

### Bước 3: Chạy Server

```bash
python app.py
```

**Output:**

```
Initializing Model for API...
Loading model from models/roberta_toxic...
Model loaded successfully!
Server running at http://127.0.0.1:5000
```
