"""
Unit tests for the Toxic Phrase Detection Model.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import ToxicPhraseDetector


class TestToxicPhraseDetector(unittest.TestCase):
    """Test cases for ToxicPhraseDetector class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the detector once for all tests."""
        cls.detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    def test_initialization(self):
        """Test that the detector initializes correctly."""
        self.assertIsNotNone(self.detector.toxic_phrases)
        self.assertGreater(len(self.detector.toxic_phrases), 0)
        self.assertIsNotNone(self.detector.toxic_data)
    
    def test_clean_sentence(self):
        """Test detection on clean sentences without toxic phrases."""
        test_cases = [
            "This is a wonderful day!",
            "I love programming",
            "Thank you for your help",
            "The weather is beautiful",
        ]
        
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertFalse(result['is_toxic'], f"Expected non-toxic for: {sentence}")
                self.assertEqual(result['toxic_count'], 0)
                self.assertEqual(len(result['toxic_phrases']), 0)
    
    def test_single_toxic_phrase(self):
        """Test detection of single toxic phrase."""
        test_cases = [
            ("This is pure brainrot", "brainrot"),
            ("Stop posting ragebait", "ragebait"),
            ("I got downvoted", "downvoted"),
            ("Those tankies are wrong", "tankies"),
        ]
        
        for sentence, expected_phrase in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic for: {sentence}")
                self.assertEqual(result['toxic_count'], 1)
                self.assertIn(expected_phrase, result['toxic_phrases'])
    
    def test_multiple_toxic_phrases(self):
        """Test detection of multiple toxic phrases in one sentence."""
        test_cases = [
            ("This ragebait is pure brainrot", 2),
            ("Stop downvoting this ragebait content", 2),
            ("The autists and tankies are arguing", 2),
            ("Downvoted for brainrot ragebait", 3),
        ]
        
        for sentence, expected_count in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic for: {sentence}")
                self.assertEqual(result['toxic_count'], expected_count,
                               f"Expected {expected_count} toxic phrases in: {sentence}")
    
    def test_case_insensitivity(self):
        """Test that detection is case-insensitive."""
        test_cases = [
            "BRAINROT",
            "BrainRot",
            "brainrot",
            "RAGEBAIT",
            "RageBait",
        ]
        
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic for: {sentence}")
                self.assertGreater(result['toxic_count'], 0)
    
    def test_word_boundaries(self):
        """Test that word boundaries are respected."""
        # These should detect the toxic phrase
        positive_cases = [
            "downvote this",
            "the downvote was unfair",
            "stop downvoting",
        ]
        
        for sentence in positive_cases:
            with self.subTest(sentence=sentence, expected=True):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic for: {sentence}")
    
    def test_return_details(self):
        """Test that detailed results are returned when requested."""
        sentence = "This ragebait is pure brainrot"
        result = self.detector.detect(sentence, return_details=True)
        
        self.assertIn('details', result)
        self.assertIsInstance(result['details'], list)
        self.assertGreater(len(result['details']), 0)
        
        # Check detail structure
        for detail in result['details']:
            self.assertIn('phrase', detail)
            self.assertIn('position', detail)
            self.assertIn('canonical_form', detail)
            self.assertIn('type', detail)
            self.assertIn('toxic_score', detail)
    
    def test_batch_detection(self):
        """Test batch detection on multiple sentences."""
        sentences = [
            "This is clean",
            "This is brainrot",
            "This ragebait is pure brainrot",
        ]
        
        results = self.detector.batch_detect(sentences)
        
        self.assertEqual(len(results), len(sentences))
        self.assertFalse(results[0]['is_toxic'])
        self.assertTrue(results[1]['is_toxic'])
        self.assertTrue(results[2]['is_toxic'])
        self.assertEqual(results[1]['toxic_count'], 1)
        self.assertEqual(results[2]['toxic_count'], 2)
    
    def test_empty_string(self):
        """Test detection on empty string."""
        result = self.detector.detect("")
        self.assertFalse(result['is_toxic'])
        self.assertEqual(result['toxic_count'], 0)
    
    def test_whitespace_handling(self):
        """Test that extra whitespace is handled correctly."""
        sentence1 = "This   is   brainrot"
        sentence2 = "This is brainrot"
        
        result1 = self.detector.detect(sentence1)
        result2 = self.detector.detect(sentence2)
        
        self.assertEqual(result1['is_toxic'], result2['is_toxic'])
        self.assertEqual(result1['toxic_count'], result2['toxic_count'])
    
    def test_statistics(self):
        """Test that statistics are generated correctly."""
        stats = self.detector.get_statistics()
        
        self.assertIn('total_toxic_phrases', stats)
        self.assertIn('total_entries', stats)
        self.assertIn('by_type', stats)
        self.assertIn('avg_toxic_score', stats)
        self.assertIn('max_toxic_score', stats)
        self.assertIn('min_toxic_score', stats)
        
        self.assertGreater(stats['total_toxic_phrases'], 0)
        self.assertGreater(stats['total_entries'], 0)
    
    def test_positive_slang_not_toxic(self):
        """Test that positive slang with low scores are not marked as toxic."""
        # goated and brofist are positive with score 1 (below threshold 3)
        test_cases = [
            "That play was goated!",
            "Brofist to my friends",
        ]
        
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                # These should not be toxic since they're positive and score < 3
                self.assertFalse(result['is_toxic'], f"Expected non-toxic for: {sentence}")
    
    def test_threshold_filtering(self):
        """Test that threshold filtering works correctly."""
        # Create detector with different threshold
        detector_low = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=2)
        detector_high = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=4)
        
        # downvote has score 2 and type negative
        sentence = "I got downvoted"
        
        # Should be detected by low threshold (includes negative types)
        result_low = detector_low.detect(sentence)
        self.assertTrue(result_low['is_toxic'])
        
        # Should be detected by high threshold (includes negative types)
        result_high = detector_high.detect(sentence)
        self.assertTrue(result_high['is_toxic'])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the detector once for all tests."""
        cls.detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    def test_repeated_toxic_phrase(self):
        """Test that repeated toxic phrases are counted multiple times."""
        sentence = "brainrot brainrot brainrot"
        result = self.detector.detect(sentence)
        
        self.assertTrue(result['is_toxic'])
        self.assertEqual(result['toxic_count'], 3)
    
    def test_punctuation_handling(self):
        """Test detection with various punctuation."""
        test_cases = [
            "This is brainrot!",
            "What is this ragebait?",
            "Stop the brainrot.",
            "This (ragebait) is bad",
        ]
        
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                result = self.detector.detect(sentence)
                self.assertTrue(result['is_toxic'], f"Expected toxic for: {sentence}")
    
    def test_special_characters(self):
        """Test handling of special characters."""
        sentence = "This is @#$% brainrot content"
        result = self.detector.detect(sentence)
        self.assertTrue(result['is_toxic'])
    
    def test_unicode_text(self):
        """Test detection with unicode characters."""
        sentence = "This is brainrot 😂🤣"
        result = self.detector.detect(sentence)
        self.assertTrue(result['is_toxic'])


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestToxicPhraseDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
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
