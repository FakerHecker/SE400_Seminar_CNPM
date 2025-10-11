"""
Additional unit tests for root words and leetspeak variations.
These tests verify the improved detection capabilities.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import ToxicPhraseDetector


class TestRootWordsDetection(unittest.TestCase):
    """Test cases for root word detection."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the detector once for all tests."""
        cls.detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    def test_basic_root_words(self):
        """Test that basic toxic root words are detected."""
        root_words = ['fuck', 'fck', 'shit', 'damn', 'hell', 'bitch', 'ass', 'bastard', 'crap']
        
        for word in root_words:
            with self.subTest(word=word):
                result = self.detector.detect(word)
                self.assertTrue(result['is_toxic'], f"Expected '{word}' to be toxic")
                self.assertEqual(result['toxic_count'], 1)
    
    def test_root_words_case_insensitive(self):
        """Test that root words work with different cases."""
        test_cases = [
            ('fuck', True),
            ('FUCK', True),
            ('Fuck', True),
            ('FuCk', True),
            ('fck', True),
            ('FCK', True),
        ]
        
        for word, expected_toxic in test_cases:
            with self.subTest(word=word):
                result = self.detector.detect(word)
                self.assertEqual(result['is_toxic'], expected_toxic)
    
    def test_root_words_in_context(self):
        """Test that root words are detected in sentences."""
        test_cases = [
            'What the fuck is this',
            'This is fck annoying',
            'Oh shit',
            'Damn it',
            'Go to hell',
        ]
        
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic in: {sentence}")
                self.assertGreater(result['toxic_count'], 0)


class TestLeetspeakDetection(unittest.TestCase):
    """Test cases for leetspeak variation detection."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the detector once for all tests."""
        cls.detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    def test_number_substitutions(self):
        """Test detection of number-based leetspeak."""
        test_cases = [
            ('f0ck', True),   # 0 -> o
            ('sh1t', True),   # 1 -> i
            ('h3ll', True),   # 3 -> e
            ('a55', True),    # 5 -> s
        ]
        
        for word, expected_toxic in test_cases:
            with self.subTest(word=word):
                result = self.detector.detect(word)
                self.assertEqual(result['is_toxic'], expected_toxic, f"Failed for: {word}")
    
    def test_special_char_substitutions(self):
        """Test detection of special character leetspeak."""
        test_cases = [
            ('@ss', True),    # @ -> a
            ('$hit', True),   # $ -> s
            ('sh!t', True),   # ! -> i
        ]
        
        for word, expected_toxic in test_cases:
            with self.subTest(word=word):
                result = self.detector.detect(word)
                self.assertEqual(result['is_toxic'], expected_toxic, f"Failed for: {word}")
    
    def test_common_misspellings(self):
        """Test detection of common intentional misspellings."""
        test_cases = [
            ('fuk', True),
            ('phuck', True),
            ('sht', True),
        ]
        
        for word, expected_toxic in test_cases:
            with self.subTest(word=word):
                result = self.detector.detect(word)
                self.assertEqual(result['is_toxic'], expected_toxic, f"Failed for: {word}")
    
    def test_leetspeak_in_context(self):
        """Test leetspeak detection in sentences."""
        test_cases = [
            'What the f0ck is this',
            'Oh sh1t here we go',
            'You are such a b1tch',
        ]
        
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic in: {sentence}")


class TestDetailedResults(unittest.TestCase):
    """Test detailed results for variations."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the detector once for all tests."""
        cls.detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    def test_matched_as_field(self):
        """Test that matched_as field is present for variations."""
        result = self.detector.detect('f0ck', return_details=True)
        
        self.assertTrue(result['is_toxic'])
        self.assertIn('details', result)
        self.assertGreater(len(result['details']), 0)
        
        detail = result['details'][0]
        self.assertIn('matched_as', detail)
        self.assertEqual(detail['matched_as'], 'fuck')
    
    def test_direct_match_vs_variation(self):
        """Test difference between direct matches and variations."""
        # Direct match
        result_direct = self.detector.detect('fuck', return_details=True)
        self.assertTrue(result_direct['is_toxic'])
        
        # Variation match
        result_variation = self.detector.detect('f0ck', return_details=True)
        self.assertTrue(result_variation['is_toxic'])
        
        # Both should be toxic
        self.assertEqual(result_direct['is_toxic'], result_variation['is_toxic'])


class TestMultipleVariations(unittest.TestCase):
    """Test sentences with multiple toxic variations."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the detector once for all tests."""
        cls.detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    def test_multiple_root_words(self):
        """Test detection of multiple root words in one sentence."""
        result = self.detector.detect('fuck this shit')
        
        self.assertTrue(result['is_toxic'])
        self.assertEqual(result['toxic_count'], 2)
    
    def test_mixed_variations_and_root_words(self):
        """Test mix of variations and root words."""
        result = self.detector.detect('f0ck this sh1t')
        
        self.assertTrue(result['is_toxic'])
        self.assertGreaterEqual(result['toxic_count'], 2)
    
    def test_multiple_same_variation(self):
        """Test repeated toxic words."""
        result = self.detector.detect('fuck fuck fuck')
        
        self.assertTrue(result['is_toxic'])
        self.assertEqual(result['toxic_count'], 3)


def run_tests():
    """Run all additional tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestRootWordsDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestLeetspeakDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestDetailedResults))
    suite.addTests(loader.loadTestsFromTestCase(TestMultipleVariations))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("ADDITIONAL TESTS SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
