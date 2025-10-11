"""Comprehensive test for various toxic word obfuscations."""

from model import ToxicPhraseDetector

def test_comprehensive_variations():
    """Test comprehensive variations of toxic words."""
    
    print("=" * 80)
    print("COMPREHENSIVE TOXIC WORD VARIATION TESTING")
    print("=" * 80)
    
    detector = ToxicPhraseDetector('slang.csv')
    
    test_categories = {
        "Basic root words": [
            'fck', 'fuck', 'shit', 'damn', 'hell', 'bitch', 'ass', 'bastard', 'crap'
        ],
        "Leetspeak variations": [
            'f0ck', 'fuk', 'phuck', 'sh1t', 'sh!t', '$hit', 'a55', '@ss', 'h3ll', 'b1tch'
        ],
        "In context": [
            'This is fck annoying',
            'What the f0ck is this',
            'Oh sh1t',
            'You are such a b1tch',
            'This is a55 backwards',
            'Go to h3ll',
        ],
        "Multiple toxic words": [
            'fuck this shit',
            'damn fck',
            'What the hell is this shit',
        ],
        "Clean sentences (should NOT detect)": [
            'This is a nice day',
            'Thank you very much',
            'I appreciate your help',
            'The weather is beautiful',
        ],
        "Edge cases": [
            'fuckton',  # neutral, score=2, should NOT be toxic
            'fuckes',   # negative, score=3, should be toxic
            'fcks',     # negative, score=3, should be toxic
            'FUCK',     # uppercase
            'FcK',      # mixed case
            'f u c k',  # spaced (might not detect - acceptable)
        ]
    }
    
    print()
    total_tests = 0
    total_toxic = 0
    total_clean = 0
    
    for category, tests in test_categories.items():
        print(f"\n{'─' * 80}")
        print(f"Category: {category}")
        print('─' * 80)
        
        for test in tests:
            total_tests += 1
            result = detector.detect(test, return_details=True)
            status = "✓ TOXIC" if result['is_toxic'] else "○ CLEAN"
            
            if result['is_toxic']:
                total_toxic += 1
            else:
                total_clean += 1
            
            print(f"{status} | {test:40} | Count: {result['toxic_count']}")
            
            if result['toxic_phrases']:
                phrases_str = ', '.join(result['toxic_phrases'])
                print(f"       └─ Detected: {phrases_str}")
                
                # Show if matched through variation
                if result.get('details'):
                    for detail in result['details']:
                        if detail.get('matched_as') and detail.get('matched_as') != detail['phrase']:
                            print(f"          ({detail['phrase']} → {detail['matched_as']})")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY")
    print("=" * 80)
    print(f"Total tests:  {total_tests}")
    print(f"Toxic found:  {total_toxic}")
    print(f"Clean found:  {total_clean}")
    print("=" * 80)


if __name__ == "__main__":
    test_comprehensive_variations()
