"""
Toxic Phrase Detection Model
Detects toxic words/phrases in input sentences based on a slang dictionary.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Set


class ToxicPhraseDetector:
    """
    A model that detects toxic phrases in text based on a slang dictionary.
    
    Attributes:
        toxic_phrases (Set[str]): Set of toxic phrases loaded from the dictionary
        toxic_data (pd.DataFrame): Full dataframe with toxic phrase information
        toxic_threshold (int): Minimum toxic_score to consider a phrase toxic
    """
    
    def __init__(self, slang_csv_path: str = "slang.csv", toxic_threshold: int = 3):
        """
        Initialize the toxic phrase detector.
        
        Args:
            slang_csv_path: Path to the slang CSV file
            toxic_threshold: Minimum toxic_score to consider a phrase as toxic (default: 3)
        """
        self.toxic_threshold = toxic_threshold
        self.toxic_phrases = set()
        self.toxic_data = None
        self.phrase_info = {}
        self._load_toxic_phrases(slang_csv_path)
    
    def _load_toxic_phrases(self, csv_path: str):
        """Load toxic phrases from the CSV file."""
        try:
            df = pd.read_csv(csv_path)
            
            # Filter toxic phrases based on:
            # 1. type == 'negative' OR
            # 2. toxic_score >= threshold
            toxic_df = df[
                (df['type'] == 'negative') | 
                (df['toxic_score'] >= self.toxic_threshold)
            ]
            
            self.toxic_data = toxic_df
            
            # Common toxic root words and their variations
            # These will be added even if not explicitly in the dictionary
            toxic_roots = {
                'fuck': {'type': 'negative', 'score': 4},
                'fck': {'type': 'negative', 'score': 4},
                'shit': {'type': 'negative', 'score': 3},
                'damn': {'type': 'negative', 'score': 3},
                'hell': {'type': 'negative', 'score': 3},
                'bitch': {'type': 'negative', 'score': 4},
                'ass': {'type': 'negative', 'score': 3},
                'bastard': {'type': 'negative', 'score': 3},
                'crap': {'type': 'negative', 'score': 3},
            }
            
            # Store both slang and canonical_form
            for _, row in toxic_df.iterrows():
                slang = str(row['slang']).lower().strip()
                canonical = str(row['canonical_form']).lower().strip()
                
                self.toxic_phrases.add(slang)
                if canonical != slang and pd.notna(canonical):
                    self.toxic_phrases.add(canonical)
                
                # Store phrase info for detailed results
                self.phrase_info[slang] = {
                    'canonical_form': canonical,
                    'type': row['type'],
                    'toxic_score': row['toxic_score']
                }
                if canonical != slang and pd.notna(canonical):
                    self.phrase_info[canonical] = {
                        'canonical_form': canonical,
                        'type': row['type'],
                        'toxic_score': row['toxic_score']
                    }
                
                # Extract root words from compound toxic phrases
                # e.g., "fcks" -> add "fck", "buttfuck" -> add "fuck"
                for root_word, root_info in toxic_roots.items():
                    if root_word in slang:
                        if root_word not in self.toxic_phrases:
                            self.toxic_phrases.add(root_word)
                            self.phrase_info[root_word] = {
                                'canonical_form': root_word,
                                'type': root_info['type'],
                                'toxic_score': root_info['score']
                            }
            
            # Ensure all root words are included
            for root_word, root_info in toxic_roots.items():
                if root_word not in self.toxic_phrases:
                    self.toxic_phrases.add(root_word)
                    self.phrase_info[root_word] = {
                        'canonical_form': root_word,
                        'type': root_info['type'],
                        'toxic_score': root_info['score']
                    }
            
            print(f"Loaded {len(self.toxic_phrases)} unique toxic phrases from {len(toxic_df)} entries (including root words)")
            
        except Exception as e:
            print(f"Error loading toxic phrases: {e}")
            raise
    
    def _tokenize_and_normalize(self, text: str) -> str:
        """
        Normalize and prepare text for detection.
        
        Args:
            text: Input text to normalize
            
        Returns:
            Normalized text in lowercase
        """
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _expand_leetspeak_variations(self, text: str) -> List[str]:
        """
        Generate variations of text to catch leetspeak/intentional misspellings.
        
        Args:
            text: Input text
            
        Returns:
            List of text variations
        """
        variations = [text]
        
        # First, check for common intentional misspellings
        # fuk -> fuck, fck -> fuck
        misspelling_map = {
            'fuk': 'fuck',
            'fck': 'fuck',
            'f0ck': 'fuck',
            'fock': 'fuck',
            'phuck': 'fuck',
            'sht': 'shit',
            'shlt': 'shit',
            'sh1t': 'shit',
            'dmn': 'damn',
            'hll': 'hell',
            'h3ll': 'hell',
            'btch': 'bitch',
            'b1tch': 'bitch',
            'azz': 'ass',
            'a55': 'ass',
            '@ss': 'ass',
        }
        
        # Check if any misspelling pattern matches
        for misspell, correct in misspelling_map.items():
            if text == misspell:
                if correct not in variations:
                    variations.append(correct)
        
        # Common leetspeak and obfuscation patterns
        replacements = {
            '0': ['o'],
            '1': ['i', 'l'],
            '3': ['e'],
            '4': ['a'],
            '5': ['s'],
            '7': ['t'],
            '8': ['b'],
            '@': ['a'],
            '$': ['s'],
            '!': ['i'],
            '|': ['l', 'i'],
        }
        
        # Apply each replacement
        current_variations = [text]
        
        for char, replacements_list in replacements.items():
            if char in text:
                new_variations = []
                for var in current_variations:
                    for replacement in replacements_list:
                        new_var = var.replace(char, replacement)
                        if new_var not in variations:
                            variations.append(new_var)
                            # Check if this new variation maps to a known word
                            if new_var in misspelling_map:
                                correct_form = misspelling_map[new_var]
                                if correct_form not in variations:
                                    variations.append(correct_form)
                            new_variations.append(new_var)
                current_variations.extend(new_variations)
        
        return variations
    
    def detect(self, sentence: str, return_details: bool = False) -> Dict:
        """
        Detect toxic phrases in a sentence.
        
        Args:
            sentence: Input sentence to analyze
            return_details: If True, return detailed information about each toxic phrase
            
        Returns:
            Dictionary with:
                - is_toxic (bool): Whether the sentence contains toxic phrases
                - toxic_count (int): Number of toxic phrases found
                - toxic_phrases (List[str]): List of toxic phrases found
                - details (List[Dict]): Detailed info about each phrase (if return_details=True)
        """
        normalized_sentence = self._tokenize_and_normalize(sentence)
        
        found_toxic_phrases = []
        phrase_details = []
        detected_positions = set()  # Track positions to avoid duplicates
        
        # Check for each toxic phrase in the sentence
        # Use word boundaries to avoid partial matches
        for phrase in self.toxic_phrases:
            # Create pattern with word boundaries
            pattern = r'\b' + re.escape(phrase) + r'\b'
            matches = re.finditer(pattern, normalized_sentence)
            
            for match in matches:
                position = match.start()
                # Avoid counting the same position multiple times
                if position not in detected_positions:
                    detected_positions.add(position)
                    found_toxic_phrases.append(phrase)
                    if return_details and phrase in self.phrase_info:
                        phrase_details.append({
                            'phrase': phrase,
                            'position': position,
                            'canonical_form': self.phrase_info[phrase]['canonical_form'],
                            'type': self.phrase_info[phrase]['type'],
                            'toxic_score': self.phrase_info[phrase]['toxic_score']
                        })
        
        # Also check for leetspeak/obfuscated variations
        # Split sentence into words to check each word
        words = normalized_sentence.split()
        for word_idx, word in enumerate(words):
            # Skip if already detected
            word_position = normalized_sentence.find(word)
            if word_position in detected_positions:
                continue
                
            # Clean word from punctuation but keep for position tracking
            clean_word = re.sub(r'[^\w@$!]', '', word)  # Keep @, $, ! for leetspeak
            
            # Check variations
            variations = self._expand_leetspeak_variations(clean_word)
            for variation in variations:
                if variation in self.toxic_phrases:
                    detected_positions.add(word_position)
                    found_toxic_phrases.append(clean_word)  # Use original word
                    if return_details:
                        # Use the info from the matched variation
                        phrase_info = self.phrase_info.get(variation, {
                            'canonical_form': variation,
                            'type': 'negative',
                            'toxic_score': 3
                        })
                        phrase_details.append({
                            'phrase': clean_word,
                            'matched_as': variation,
                            'position': word_position,
                            'canonical_form': phrase_info['canonical_form'],
                            'type': phrase_info['type'],
                            'toxic_score': phrase_info['toxic_score']
                        })
                    break  # Found a match, no need to check other variations
        
        result = {
            'is_toxic': len(found_toxic_phrases) > 0,
            'toxic_count': len(found_toxic_phrases),
            'toxic_phrases': found_toxic_phrases
        }
        
        if return_details:
            result['details'] = phrase_details
        
        return result
    
    def batch_detect(self, sentences: List[str]) -> List[Dict]:
        """
        Detect toxic phrases in multiple sentences.
        
        Args:
            sentences: List of sentences to analyze
            
        Returns:
            List of detection results for each sentence
        """
        return [self.detect(sentence) for sentence in sentences]
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about loaded toxic phrases.
        
        Returns:
            Dictionary with statistics
        """
        if self.toxic_data is None:
            return {}
        
        return {
            'total_toxic_phrases': len(self.toxic_phrases),
            'total_entries': len(self.toxic_data),
            'by_type': self.toxic_data['type'].value_counts().to_dict(),
            'avg_toxic_score': self.toxic_data['toxic_score'].mean(),
            'max_toxic_score': self.toxic_data['toxic_score'].max(),
            'min_toxic_score': self.toxic_data['toxic_score'].min()
        }


def main():
    """CLI interface for the toxic phrase detector."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Detect toxic phrases in text')
    parser.add_argument('--text', type=str, help='Text to analyze')
    parser.add_argument('--file', type=str, help='File containing sentences to analyze (one per line)')
    parser.add_argument('--slang-csv', type=str, default='slang.csv', help='Path to slang CSV file')
    parser.add_argument('--threshold', type=int, default=3, help='Toxic score threshold')
    parser.add_argument('--details', action='store_true', help='Show detailed information')
    parser.add_argument('--stats', action='store_true', help='Show statistics about toxic phrases')
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = ToxicPhraseDetector(args.slang_csv, args.threshold)
    
    if args.stats:
        stats = detector.get_statistics()
        print("\n=== Toxic Phrase Statistics ===")
        for key, value in stats.items():
            print(f"{key}: {value}")
        print()
    
    if args.text:
        result = detector.detect(args.text, return_details=args.details)
        print(f"\nInput: {args.text}")
        print(f"Is Toxic: {result['is_toxic']}")
        print(f"Toxic Count: {result['toxic_count']}")
        if result['toxic_phrases']:
            print(f"Toxic Phrases: {', '.join(result['toxic_phrases'])}")
        if args.details and 'details' in result:
            print("\nDetails:")
            for detail in result['details']:
                print(f"  - {detail}")
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            sentences = [line.strip() for line in f if line.strip()]
        
        results = detector.batch_detect(sentences)
        print(f"\n=== Analyzing {len(sentences)} sentences ===\n")
        for i, (sentence, result) in enumerate(zip(sentences, results), 1):
            print(f"{i}. {sentence}")
            print(f"   Toxic: {result['is_toxic']} | Count: {result['toxic_count']}")
            if result['toxic_phrases']:
                print(f"   Phrases: {', '.join(result['toxic_phrases'])}")
            print()


if __name__ == "__main__":
    main()
