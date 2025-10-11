"""Test the improved toxic detection with root words and variations."""

from model import ToxicPhraseDetector

def test_root_words_and_variations():
    """Test detection of root words and their variations."""
    
    print("=" * 70)
    print("TESTING IMPROVED TOXIC PHRASE DETECTION")
    print("=" * 70)
    
    detector = ToxicPhraseDetector('slang.csv')
    
    test_cases = [
        # Root words that should now be detected
        'fck',
        'fuck',
        'Fuck',
        'FUCK',
        'shit',
        'damn',
        'hell',
        'bitch',
        'ass',
        
        # In sentences
        'Fuck you',
        'This is fck annoying',
        'What the fuck',
        'Oh shit',
        'damn it',
        'go to hell',
        
        # Variations already in dictionary
        'fcks',
        'fuckton',
        'buttfuck',
        
        # Leetspeak variations (if implemented)
        'f0ck',
        'fuk',
        'sh1t',
        'a55',
        
        # Clean sentences
        'This is a nice day',
        'Thank you very much',
    ]
    
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print()
    
    toxic_detected = 0
    clean_detected = 0
    
    for test in test_cases:
        result = detector.detect(test, return_details=True)
        status = "✓ TOXIC" if result['is_toxic'] else "○ CLEAN"
        
        if result['is_toxic']:
            toxic_detected += 1
        else:
            clean_detected += 1
        
        print(f"{status} | {test:30} | Count: {result['toxic_count']}")
        
        if result['toxic_phrases']:
            print(f"       └─ Detected: {', '.join(result['toxic_phrases'])}")
            
            if result.get('details'):
                for detail in result['details']:
                    matched_as = detail.get('matched_as', detail['phrase'])
                    if matched_as != detail['phrase']:
                        print(f"          (matched as: {matched_as})")
        print()
    
    print("=" * 70)
    print(f"Summary: {toxic_detected} toxic, {clean_detected} clean")
    print("=" * 70)


if __name__ == "__main__":
    test_root_words_and_variations()
