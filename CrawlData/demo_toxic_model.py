"""
Demo script showcasing the Toxic Phrase Detection Model
Demonstrates various use cases and features
"""

from model import ToxicPhraseDetector


def print_separator(title=""):
    """Print a separator line."""
    print("\n" + "=" * 70)
    if title:
        print(f" {title}")
        print("=" * 70)


def demo_basic_detection():
    """Demonstrate basic detection functionality."""
    print_separator("DEMO 1: Basic Detection")
    
    detector = ToxicPhraseDetector('slang.csv', toxic_threshold=3)
    
    test_sentences = [
        "This is a wonderful day!",
        "Stop posting ragebait content",
        "This movie is pure brainrot",
        "I love programming and learning",
    ]
    
    for sentence in test_sentences:
        result = detector.detect(sentence)
        print(f"\nSentence: \"{sentence}\"")
        print(f"  → Is Toxic: {result['is_toxic']}")
        print(f"  → Toxic Count: {result['toxic_count']}")
        if result['toxic_phrases']:
            print(f"  → Detected: {', '.join(result['toxic_phrases'])}")


def demo_detailed_detection():
    """Demonstrate detection with detailed information."""
    print_separator("DEMO 2: Detailed Detection")
    
    detector = ToxicPhraseDetector('slang.csv', toxic_threshold=3)
    
    sentence = "The tankies are spreading ragebait and brainrot content"
    result = detector.detect(sentence, return_details=True)
    
    print(f"\nSentence: \"{sentence}\"")
    print(f"\nToxic: {result['is_toxic']} | Count: {result['toxic_count']}")
    print("\nDetailed Information:")
    
    for detail in result['details']:
        print(f"\n  Phrase: '{detail['phrase']}'")
        print(f"    Position: {detail['position']}")
        print(f"    Canonical Form: {detail['canonical_form']}")
        print(f"    Type: {detail['type']}")
        print(f"    Toxic Score: {detail['toxic_score']}")


def demo_batch_detection():
    """Demonstrate batch processing."""
    print_separator("DEMO 3: Batch Detection")
    
    detector = ToxicPhraseDetector('slang.csv', toxic_threshold=3)
    
    sentences = [
        "Great work everyone!",
        "This ragebait is annoying",
        "I got downvoted unfairly",
        "Beautiful weather today",
        "Stop the brainrot content please",
    ]
    
    results = detector.batch_detect(sentences)
    
    print("\nProcessing multiple sentences:\n")
    toxic_count = sum(1 for r in results if r['is_toxic'])
    
    for i, (sentence, result) in enumerate(zip(sentences, results), 1):
        status = "🔴 TOXIC" if result['is_toxic'] else "🟢 CLEAN"
        print(f"{i}. {status} | \"{sentence}\"")
        if result['toxic_phrases']:
            print(f"   └─ Found: {', '.join(result['toxic_phrases'])}")
    
    print(f"\nSummary: {toxic_count}/{len(sentences)} sentences contain toxic phrases")


def demo_threshold_comparison():
    """Demonstrate different threshold settings."""
    print_separator("DEMO 4: Threshold Comparison")
    
    sentence = "I got downvoted for this comment"
    
    thresholds = [2, 3, 4]
    
    print(f"\nSentence: \"{sentence}\"")
    print("\nTesting with different thresholds:\n")
    
    for threshold in thresholds:
        detector = ToxicPhraseDetector('slang.csv', toxic_threshold=threshold)
        result = detector.detect(sentence)
        
        print(f"Threshold = {threshold}:")
        print(f"  → Toxic: {result['is_toxic']}")
        print(f"  → Count: {result['toxic_count']}")
        if result['toxic_phrases']:
            print(f"  → Phrases: {', '.join(result['toxic_phrases'])}")
        print(f"  → Total phrases loaded: {len(detector.toxic_phrases)}")
        print()


def demo_statistics():
    """Display statistics about the toxic phrase dictionary."""
    print_separator("DEMO 5: Dictionary Statistics")
    
    detector = ToxicPhraseDetector('slang.csv', toxic_threshold=3)
    stats = detector.get_statistics()
    
    print("\nToxic Phrase Dictionary Statistics:\n")
    print(f"  Total Unique Toxic Phrases: {stats['total_toxic_phrases']}")
    print(f"  Total Dictionary Entries: {stats['total_entries']}")
    print(f"\n  Distribution by Type:")
    for type_name, count in stats['by_type'].items():
        percentage = (count / stats['total_entries']) * 100
        print(f"    - {type_name}: {count} ({percentage:.1f}%)")
    
    print(f"\n  Toxic Score Statistics:")
    print(f"    - Average: {stats['avg_toxic_score']:.2f}")
    print(f"    - Minimum: {stats['min_toxic_score']}")
    print(f"    - Maximum: {stats['max_toxic_score']}")


def demo_case_sensitivity():
    """Demonstrate case-insensitive detection."""
    print_separator("DEMO 6: Case Insensitivity")
    
    detector = ToxicPhraseDetector('slang.csv', toxic_threshold=3)
    
    variations = [
        "This is brainrot content",
        "This is BRAINROT content",
        "This is BrainRot content",
        "This is BrAiNrOt content",
    ]
    
    print("\nTesting case variations:\n")
    
    for sentence in variations:
        result = detector.detect(sentence)
        print(f"  \"{sentence}\"")
        print(f"    → Detected: {result['is_toxic']} (Count: {result['toxic_count']})")


def demo_real_world_examples():
    """Demonstrate with real-world-like examples."""
    print_separator("DEMO 7: Real-World Examples")
    
    detector = ToxicPhraseDetector('slang.csv', toxic_threshold=3)
    
    examples = [
        "Just watched an amazing movie, highly recommend!",
        "Why do people keep posting this ragebait nonsense?",
        "I'm tired of all the brainrot on social media these days",
        "Thanks for the helpful explanation, really appreciate it!",
        "Another day, another downvote for speaking the truth",
        "The weather is perfect for a walk in the park today",
    ]
    
    print("\nAnalyzing real-world-like comments:\n")
    
    for i, sentence in enumerate(examples, 1):
        result = detector.detect(sentence)
        
        print(f"{i}. {sentence}")
        if result['is_toxic']:
            print(f"   ⚠️  WARNING: Contains {result['toxic_count']} toxic phrase(s)")
            print(f"   → {', '.join(result['toxic_phrases'])}")
        else:
            print(f"   ✅ Clean")
        print()


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print(" TOXIC PHRASE DETECTION MODEL - COMPREHENSIVE DEMO")
    print("=" * 70)
    print("\n This demo showcases various features of the toxic phrase detector")
    print(" including basic detection, detailed analysis, batch processing,")
    print(" threshold comparison, and real-world examples.")
    
    try:
        demo_basic_detection()
        demo_detailed_detection()
        demo_batch_detection()
        demo_threshold_comparison()
        demo_statistics()
        demo_case_sensitivity()
        demo_real_world_examples()
        
        print_separator("DEMO COMPLETE")
        print("\nAll demonstrations completed successfully!")
        print("\nTo use the model in your code:")
        print("  from model import ToxicPhraseDetector")
        print("  detector = ToxicPhraseDetector('slang.csv')")
        print("  result = detector.detect('Your sentence here')")
        print("\nFor more information, see README_TOXIC_MODEL.md")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
