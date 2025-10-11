import csv
import re
from collections import Counter
import argparse

def load_words(filepath):
    """Tải từ điển từ file, trả về một set các từ viết thường."""
    print(f"Loading dictionary from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = {line.strip().lower() for line in f if line.strip()}
        print(f"Loaded {len(words)} words.")
        return words
    except FileNotFoundError:
        print(f"Error: Dictionary file not found at {filepath}")
        return None

class SpellCorrector:
    def __init__(self, dictionary_path):
        self.WORDS = load_words(dictionary_path)
        if self.WORDS is None:
            raise FileNotFoundError("Dictionary could not be loaded.")

    def correction(self, word):
        """Tìm từ sửa lỗi có khả năng cao nhất cho một từ."""
        word = word.lower()
        # Ưu tiên 1: Từ đã đúng chính tả
        if word in self.WORDS:
            return word
        
        # Ưu tiên 2: Tìm các từ có khoảng cách chỉnh sửa là 1
        candidates_ed1 = self._edits1(word)
        known_candidates_ed1 = self._known(candidates_ed1)
        if known_candidates_ed1:
            # Nếu có nhiều ứng viên, trả về ứng viên đầu tiên tìm thấy (để đơn giản)
            # Một cách nâng cao hơn là chọn từ có tần suất cao nhất trong một kho ngữ liệu lớn
            return max(known_candidates_ed1) # Trả về từ cuối cùng theo alphabet, khá ngẫu nhiên nhưng ổn

        # Ưu tiên 3: Tìm các từ có khoảng cách chỉnh sửa là 2
        candidates_ed2 = self._edits2(word)
        known_candidates_ed2 = self._known(candidates_ed2)
        if known_candidates_ed2:
            return max(known_candidates_ed2)

        # Ưu tiên 4: Giữ nguyên từ gốc nếu không tìm thấy
        return word

    def _known(self, words):
        """Lọc ra những từ có trong từ điển."""
        return {w for w in words if w in self.WORDS}

    def _edits1(self, word):
        """Tạo ra tất cả các từ có khoảng cách chỉnh sửa là 1."""
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word):
        """Tạo ra tất cả các từ có khoảng cách chỉnh sửa là 2."""
        return (e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))

def main():
    # --- CÁC THAM SỐ CÀI ĐẶT CỨNG ---
    input_file = 'D:/CrawlData/slang_output.csv'
    output_file = 'D:/CrawlData/slang_normalized.csv'
    dict_file = 'base_dict_alternative.txt'
    # --- KẾT THÚC PHẦN CÀI ĐẶT ---

    try:
        corrector = SpellCorrector(dict_file)
    except FileNotFoundError:
        return

    print(f"Processing {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as fin, \
             open(output_file, 'w', encoding='utf-8', newline='') as fout:
            
            reader = csv.reader(fin)
            writer = csv.writer(fout)

            try:
                header = next(reader)
                writer.writerow(header + ['suggested_canon'])
            except StopIteration:
                print("Input file is empty.")
                return

            # Tìm chỉ số của cột 'slang'
            try:
                slang_col_idx = header.index('slang')
            except ValueError:
                print("Error: 'slang' column not found in input file.")
                return

            count = 0
            for row in reader:
                count += 1
                slang_word = row[slang_col_idx]
                
                # Tìm từ chuẩn hóa
                suggestion = corrector.correction(slang_word)
                
                writer.writerow(row + [suggestion])
                
                if count % 100 == 0:
                    print(f"Processed {count} words...")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return
        
    print(f"Done. Wrote {count} normalized words to {output_file}")

if __name__ == '__main__':
    main()