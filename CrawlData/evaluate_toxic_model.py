"""
Evaluation script for the Toxic Phrase Detection Model.
Tests the model on various test cases and calculates performance metrics.
"""

from model import ToxicPhraseDetector
from typing import List, Tuple
import json


class ToxicModelEvaluator:
    """Evaluator for the Toxic Phrase Detection Model."""
    
    def __init__(self, detector: ToxicPhraseDetector):
        """
        Initialize evaluator with a detector.
        
        Args:
            detector: ToxicPhraseDetector instance
        """
        self.detector = detector
    
    def evaluate(self, test_cases: List[Tuple[str, bool, int]]) -> dict:
        """
        Evaluate the model on test cases.
        
        Args:
            test_cases: List of tuples (sentence, is_toxic_label, expected_count)
            
        Returns:
            Dictionary with evaluation metrics
        """
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0
        
        correct_counts = 0
        total_expected_phrases = 0
        total_detected_phrases = 0
        
        detailed_results = []
        
        for sentence, expected_toxic, expected_count in test_cases:
            result = self.detector.detect(sentence, return_details=True)
            predicted_toxic = result['is_toxic']
            predicted_count = result['toxic_count']
            
            # Classification metrics
            if expected_toxic and predicted_toxic:
                true_positives += 1
            elif not expected_toxic and predicted_toxic:
                false_positives += 1
            elif not expected_toxic and not predicted_toxic:
                true_negatives += 1
            elif expected_toxic and not predicted_toxic:
                false_negatives += 1
            
            # Count accuracy
            if predicted_count == expected_count:
                correct_counts += 1
            
            total_expected_phrases += expected_count
            total_detected_phrases += predicted_count
            
            detailed_results.append({
                'sentence': sentence,
                'expected_toxic': expected_toxic,
                'predicted_toxic': predicted_toxic,
                'expected_count': expected_count,
                'predicted_count': predicted_count,
                'toxic_phrases': result['toxic_phrases'],
                'correct': expected_toxic == predicted_toxic and expected_count == predicted_count
            })
        
        # Calculate metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (true_positives + true_negatives) / len(test_cases) if test_cases else 0
        count_accuracy = correct_counts / len(test_cases) if test_cases else 0
        
        return {
            'total_test_cases': len(test_cases),
            'true_positives': true_positives,
            'false_positives': false_positives,
            'true_negatives': true_negatives,
            'false_negatives': false_negatives,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'count_accuracy': count_accuracy,
            'total_expected_phrases': total_expected_phrases,
            'total_detected_phrases': total_detected_phrases,
            'detailed_results': detailed_results
        }
    
    def print_evaluation_report(self, metrics: dict, show_details: bool = False):
        """Print a formatted evaluation report."""
        print("\n" + "="*60)
        print("TOXIC PHRASE DETECTION MODEL - EVALUATION REPORT")
        print("="*60)
        
        print(f"\nTotal Test Cases: {metrics['total_test_cases']}")
        print(f"\nConfusion Matrix:")
        print(f"  True Positives:  {metrics['true_positives']}")
        print(f"  False Positives: {metrics['false_positives']}")
        print(f"  True Negatives:  {metrics['true_negatives']}")
        print(f"  False Negatives: {metrics['false_negatives']}")
        
        print(f"\nPerformance Metrics:")
        print(f"  Accuracy:        {metrics['accuracy']:.2%}")
        print(f"  Precision:       {metrics['precision']:.2%}")
        print(f"  Recall:          {metrics['recall']:.2%}")
        print(f"  F1-Score:        {metrics['f1_score']:.2%}")
        print(f"  Count Accuracy:  {metrics['count_accuracy']:.2%}")
        
        print(f"\nPhrase Detection:")
        print(f"  Expected Phrases:  {metrics['total_expected_phrases']}")
        print(f"  Detected Phrases:  {metrics['total_detected_phrases']}")
        
        if show_details:
            print("\n" + "-"*60)
            print("DETAILED RESULTS:")
            print("-"*60)
            for i, result in enumerate(metrics['detailed_results'], 1):
                status = "✓" if result['correct'] else "✗"
                print(f"\n{i}. {status} {result['sentence']}")
                print(f"   Expected: Toxic={result['expected_toxic']}, Count={result['expected_count']}")
                print(f"   Predicted: Toxic={result['predicted_toxic']}, Count={result['predicted_count']}")
                if result['toxic_phrases']:
                    print(f"   Detected Phrases: {', '.join(result['toxic_phrases'])}")
        
        print("\n" + "="*60)


def create_test_cases() -> List[Tuple[str, bool, int]]:
    """
    Create test cases for evaluation.
    
    Returns:
        List of tuples (sentence, is_toxic, expected_count)
    """
    test_cases = [
        # Clean sentences (no toxic phrases)
        ("This is a wonderful day!", False, 0),
        ("I love programming and learning new things", False, 0),
        ("The weather is beautiful today", False, 0),
        ("Thank you for your help", False, 0),
        ("This is an amazing project", False, 0),
        
        # Single toxic phrase
        ("Stop posting ragebait content", True, 1),
        ("This movie is pure brainrot", True, 1),
        ("I got downvoted for my comment", True, 1),
        ("They are just gooning all day", True, 1),
        ("Those tankies are at it again", True, 1),
        
        # Multiple toxic phrases
        ("This ragebait post is pure brainrot", True, 2),
        ("Stop downvoting, this ragebait is obvious", True, 2),
        ("The autists and tankies are arguing again", True, 2),
        ("Downvoted for posting brainrot ragebait", True, 3),
        
        # Mixed content (toxic + normal)
        ("I love this game but stop posting ragebait", True, 1),
        ("This is a good discussion, no downvoting please", True, 1),
        ("Beautiful day for some brainrot content", True, 1),
        
        # Edge cases
        ("downvote", True, 1),
        ("RAGEBAIT", True, 1),  # Case insensitive
        ("This is not downvote-worthy", True, 1),  # Word boundaries
        ("I disagree but won't downvote you", True, 1),
        
        # Neutral/positive slang
        ("That play was goated!", False, 0),  # goated is positive, score 1
        ("Brofist to my fellow gamers", False, 0),  # brofist is positive, score 1
        
        # Complex sentences
        ("The tankies are spreading ragebait and brainrot content while downvoting everyone", True, 4),
        ("Please stop the gooning and focus on work", True, 1),
    ]
    
    return test_cases


def main():
    """Main evaluation function."""
    print("Initializing Toxic Phrase Detector...")
    detector = ToxicPhraseDetector(slang_csv_path='slang.csv', toxic_threshold=3)
    
    print("\nDetector Statistics:")
    stats = detector.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nCreating test cases...")
    test_cases = create_test_cases()
    
    print(f"Running evaluation on {len(test_cases)} test cases...")
    evaluator = ToxicModelEvaluator(detector)
    metrics = evaluator.evaluate(test_cases)
    
    # Print report
    evaluator.print_evaluation_report(metrics, show_details=True)
    
    # Save results to JSON
    output_file = 'evaluation_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"\nDetailed results saved to: {output_file}")
    
    # Interactive testing
    print("\n" + "="*60)
    print("INTERACTIVE TESTING")
    print("="*60)
    print("Enter sentences to test (or 'quit' to exit):\n")
    
    while True:
        try:
            user_input = input("Enter sentence: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input:
                result = detector.detect(user_input, return_details=True)
                print(f"\n  Is Toxic: {result['is_toxic']}")
                print(f"  Toxic Count: {result['toxic_count']}")
                if result['toxic_phrases']:
                    print(f"  Toxic Phrases: {', '.join(result['toxic_phrases'])}")
                    if result['details']:
                        print(f"  Details:")
                        for detail in result['details']:
                            print(f"    - {detail['phrase']} (score: {detail['toxic_score']}, type: {detail['type']})")
                print()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nEvaluation complete!")


if __name__ == "__main__":
    main()
