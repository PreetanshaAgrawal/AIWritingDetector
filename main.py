import re
from collections import Counter
from writing_samples import writing_detector_data, writing_styles

def wordAnalysis(text):
    """Analyze text for AI writing indicators with improved efficiency and accuracy"""
    if not text or len(text.strip()) == 0:
        return 0
    
    text_lower = text.lower()
    text_length = len(text.split())  # Word count for normalization
    
    matched_phrases = {}
    total_matches = 0
    
    # Check each category with weighted scoring
    weights = {
        "filler_phrases": 3,
        "credibility_markers": 2,
        "descriptive_overuse": 2,
        "attribution_patterns": 1,
        "structural_patterns": 4,
        "commonly_overused_words": 1,
        "common_constructions": 3,
    }
    
    for category, indicators in writing_detector_data["ai_writing_indicators"].items():
        matched_phrases[category] = []
        weight = weights.get(category, 1)
        
        for indicator in indicators:
            # Use word boundaries for better accuracy
            pattern = r'\b' + re.escape(indicator.lower()) + r'\b'
            matches = len(re.findall(pattern, text_lower))
            
            if matches > 0:
                matched_phrases[category].append({
                    "phrase": indicator,
                    "count": matches,
                    "weight": weight
                })
                total_matches += matches * weight
    
    # Normalize score to 0-100 range
    # Higher word count = lower percentage (harder to be 100% AI)
    normalization_factor = max(text_length / 100, 1)
    raw_score = total_matches / normalization_factor
    
    # Cap at 100%
    final_score = min(raw_score, 100)
    
    return final_score, matched_phrases


def displayResults(score, matched_phrases):
    """Display analysis results in a readable format"""
    print(f"\n{'='*60}")
    print(f"AI Writing Detection Result: {score:.1f}%")
    print(f"{'='*60}\n")
    
    if score < 20:
        assessment = "Likely HUMAN-written"
    elif score < 50:
        assessment = "Possibly human-written with some AI characteristics"
    elif score < 80:
        assessment = "Likely AI-assisted or heavily edited"
    else:
        assessment = "Likely AI-generated"
    
    print(f"Assessment: {assessment}\n")
    
    # Show matched phrases by category
    for category, matches in matched_phrases.items():
        if matches:
            print(f"{category.upper().replace('_', ' ')}:")
            for item in matches:
                print(f"  - '{item['phrase']}' (found {item['count']} time(s))")
            print()


if __name__ == "__main__":
    print("AI Writing Detector")
    print("="*60)
    text = input("Enter the text to analyze: ").strip()
    
    if text:
        score, matched_phrases = wordAnalysis(text)
        displayResults(score, matched_phrases)
    else:
        print("Error: Please enter valid text to analyze") 