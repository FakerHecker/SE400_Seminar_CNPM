import csv
import re
from collections import Counter
# import argparse # Không cần dùng nữa

# Regex để tách từ (token)
TOKEN_RE = re.compile(r'\b[a-zA-Z-]+\b')

# Các cột văn bản mặc định cần xử lý
DEFAULT_TEXT_COLUMNS = ['text', 'body', 'selftext', 'comment', 'content']

def load_base_dict(filepath):
    """Tải từ điển cơ sở vào một set để tra cứu nhanh."""
    print(f"Loading base dictionary from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Đọc, bỏ khoảng trắng, và chuyển thành chữ thường
            return {line.strip().lower() for line in f}
    except FileNotFoundError:
        print(f"Error: Base dictionary file not found at {filepath}")
        print("Please make sure 'base_dict_alternative.txt' is in the same directory.")
        return set()

def canonicalize_token(token):
    """Chuẩn hóa token về dạng cơ bản (chữ thường, bỏ ký tự lặp)."""
    token = token.lower()
    # Thay thế 3+ ký tự lặp bằng 2 ký tự (ví dụ: heloooo -> heloo)
    token = re.sub(r'(.)\1{2,}', r'\1\1', token)
    return token

def get_text_columns_indices(header):
    """Lấy chỉ số của các cột văn bản cần xử lý từ header."""
    header_lower = [h.lower() for h in header]
    indices = []
    for col_name in DEFAULT_TEXT_COLUMNS:
        if col_name in header_lower:
            indices.append(header_lower.index(col_name))
    
    if not indices and len(header) > 1:
        print(f"Warning: No default text columns found. Falling back to processing column index 1 ('{header[1]}').")
        return [1]
    return indices

def main():
    # --- CÁC THAM SỐ ĐÃ ĐƯỢC CÀI ĐẶT CỨNG ---
    input_file = 'D:/CrawlData/reddit_data_nolinks.csv'
    output_file = 'D:/CrawlData/slang_output.csv'
    dict_file = 'base_dict_alternative.txt'
    min_freq = 1
    # --- KẾT THÚC PHẦN CÀI ĐẶT ---

    # Phần code `argparse` đã được loại bỏ.
    
    base_dict = load_base_dict(dict_file)
    if not base_dict:
        return
    print(f"Loaded {len(base_dict)} unique tokens into dictionary.")

    slang_candidates = Counter()
    total_rows = 0

    print(f"Processing {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("Input file is empty.")
                return
                
            text_col_indices = get_text_columns_indices(header)
            if not text_col_indices:
                print("Error: Could not determine which column to process. Please check column names.")
                return

            for row in reader:
                total_rows += 1
                for col_idx in text_col_indices:
                    if col_idx < len(row):
                        text = row[col_idx]
                        tokens = TOKEN_RE.findall(text)
                        for token in tokens:
                            if not (2 < len(token) < 20):
                                continue
                            
                            lower_token = token.lower()
                            canon_token = canonicalize_token(lower_token)
                            
                            if not lower_token.isnumeric() and lower_token not in base_dict and canon_token not in base_dict:
                                slang_candidates[lower_token] += 1
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return

    print(f"Processed {total_rows} rows.")
    print(f"Found {len(slang_candidates)} potential slang candidates.")

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['slang', 'frequency', 'canonical_form'])
        
        count_written = 0
        for token, freq in slang_candidates.most_common():
            if freq >= min_freq:
                canon_form = canonicalize_token(token)
                writer.writerow([token, freq, canon_form])
                count_written += 1
    
    print(f"Wrote {count_written} slang words (frequency >= {min_freq}) to {output_file}")

if __name__ == '__main__':
    main()