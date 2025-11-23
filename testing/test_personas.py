#!/usr/bin/env python3
"""
Black Box Testing for PALETTE-AI
Tests the questionnaire with known personas and validates output
"""

import requests
import json
from typing import Dict, Any

# API endpoint
API_URL = "http://localhost:8001/api/submit"

# Test Personas with Expected Results
PERSONAS = [
    {
        "name": "Sofia - Classic Cool Summer",
        "input": {
            "first_name": "Sofia",
            "last_name": "Test",
            "email": "sofia@test.com",
            "language": "en",
            "privacy_consent": True,
            "newsletter_consent": False,

            "hair_color": "ash_blonde",
            "skin_tone": "fair",
            "eye_color": "light_blue",
            "vein_color": "blue_purple",
            "jewelry_preference": "silver",
            "colors_worn": ["pastels", "muted_colors"],
            "colors_avoided": ["bright_jewel_tones", "black_navy_charcoal"],
            "color_feedback": "depends"
        },
        "expected": {
            "undertone": "cool",
            "season_family": ["light_summer", "true_summer", "soft_summer"]
        }
    },

    {
        "name": "Marco - Deep Warm Autumn",
        "input": {
            "first_name": "Marco",
            "last_name": "Test",
            "email": "marco@test.com",
            "language": "en",
            "privacy_consent": True,
            "newsletter_consent": False,

            "hair_color": "dark_brown",
            "skin_tone": "medium_olive",
            "eye_color": "dark_brown",
            "vein_color": "green_olive",
            "jewelry_preference": "gold",
            "colors_worn": ["earth_tones", "brown_beige_camel"],
            "colors_avoided": ["pastels", "bright_jewel_tones"],
            "color_feedback": "depends"
        },
        "expected": {
            "undertone": "warm",
            "season_family": ["true_autumn", "dark_autumn", "soft_autumn"]
        }
    },

    {
        "name": "Elena - Bright Cool Winter",
        "input": {
            "first_name": "Elena",
            "last_name": "Test",
            "email": "elena@test.com",
            "language": "en",
            "privacy_consent": True,
            "newsletter_consent": False,

            "hair_color": "black",
            "skin_tone": "very_fair",
            "eye_color": "light_blue",
            "vein_color": "blue_purple",
            "jewelry_preference": "silver",
            "colors_worn": ["black_navy_charcoal", "bright_jewel_tones"],
            "colors_avoided": ["earth_tones", "pastels"],
            "color_feedback": "vibrant_glowing"
        },
        "expected": {
            "undertone": "cool",
            "season_family": ["bright_winter", "true_winter", "dark_winter"]
        }
    },

    {
        "name": "Giulia - Warm Spring",
        "input": {
            "first_name": "Giulia",
            "last_name": "Test",
            "email": "giulia@test.com",
            "language": "en",
            "privacy_consent": True,
            "newsletter_consent": False,

            "hair_color": "golden_blonde",
            "skin_tone": "fair",
            "eye_color": "green",
            "vein_color": "green_olive",
            "jewelry_preference": "gold",
            "colors_worn": ["pastels", "earth_tones"],
            "colors_avoided": ["black_navy_charcoal"],
            "color_feedback": "vibrant_glowing"
        },
        "expected": {
            "undertone": "warm",
            "season_family": ["bright_spring", "light_spring", "true_spring"]
        }
    },

    {
        "name": "Luca - Neutral (Edge Case)",
        "input": {
            "first_name": "Luca",
            "last_name": "Test",
            "email": "luca@test.com",
            "language": "en",
            "privacy_consent": True,
            "newsletter_consent": False,

            "hair_color": "light_brown",
            "skin_tone": "light_medium",
            "eye_color": "hazel",
            "vein_color": "both_not_sure",
            "jewelry_preference": "both_look_good",
            "colors_worn": ["pastels", "muted_colors", "earth_tones"],
            "colors_avoided": ["bright_jewel_tones"],
            "color_feedback": "depends"
        },
        "expected": {
            "undertone": "neutral",
            "season_family": ["soft_summer", "soft_autumn"]
        }
    }
]


def test_persona(persona: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single persona and return results"""
    print(f"\n{'='*60}")
    print(f"Testing: {persona['name']}")
    print(f"{'='*60}")

    try:
        # Submit to API
        response = requests.post(API_URL, json=persona['input'])

        if response.status_code != 200:
            return {
                "persona": persona['name'],
                "status": "FAILED",
                "error": f"HTTP {response.status_code}: {response.text}"
            }

        result = response.json()

        # Extract results
        actual_season = result.get('season')
        actual_undertone = result.get('undertone')
        actual_confidence = result.get('confidence')

        # Check if result matches expectations
        expected_undertone = persona['expected']['undertone']
        expected_seasons = persona['expected']['season_family']

        undertone_match = actual_undertone == expected_undertone
        season_match = actual_season in expected_seasons

        # Determine pass/fail
        if undertone_match and season_match:
            status = "✅ PASS"
        elif undertone_match:
            status = "⚠️  PARTIAL (undertone correct, season unexpected)"
        else:
            status = "❌ FAIL"

        # Print results
        print(f"\nInput Summary:")
        print(f"  Hair: {persona['input']['hair_color']}")
        print(f"  Skin: {persona['input']['skin_tone']}")
        print(f"  Eyes: {persona['input']['eye_color']}")
        print(f"  Veins: {persona['input']['vein_color']}")
        print(f"  Jewelry: {persona['input']['jewelry_preference']}")

        print(f"\nExpected:")
        print(f"  Undertone: {expected_undertone}")
        print(f"  Season: {' OR '.join(expected_seasons)}")

        print(f"\nActual Result:")
        print(f"  Season: {actual_season}")
        print(f"  Undertone: {actual_undertone}")
        print(f"  Confidence: {actual_confidence}%")
        print(f"  Value: {result.get('value')}")
        print(f"  Chroma: {result.get('chroma')}")

        print(f"\n{status}")

        return {
            "persona": persona['name'],
            "status": status,
            "expected_undertone": expected_undertone,
            "actual_undertone": actual_undertone,
            "expected_seasons": expected_seasons,
            "actual_season": actual_season,
            "confidence": actual_confidence,
            "undertone_match": undertone_match,
            "season_match": season_match
        }

    except Exception as e:
        return {
            "persona": persona['name'],
            "status": "ERROR",
            "error": str(e)
        }


def main():
    """Run all persona tests"""
    print("\n" + "="*60)
    print("PALETTE-AI Black Box Testing")
    print("Testing algorithm with known personas")
    print("="*60)

    results = []
    for persona in PERSONAS:
        result = test_persona(persona)
        results.append(result)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(1 for r in results if r['status'] == "✅ PASS")
    partial = sum(1 for r in results if "PARTIAL" in r['status'])
    failed = sum(1 for r in results if r['status'] == "❌ FAIL")
    errors = sum(1 for r in results if r['status'] in ["ERROR", "FAILED"])

    total = len(results)

    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"⚠️  Partial: {partial}")
    print(f"❌ Failed: {failed}")
    print(f"🔴 Errors: {errors}")

    if passed == total:
        print("\n🎉 All tests passed!")
    elif passed + partial == total:
        print("\n⚠️  Some tests partially passed - algorithm needs tuning")
    else:
        print("\n❌ Algorithm has issues - needs debugging")

    print("\n" + "="*60 + "\n")

    # Save results to JSON
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("📁 Detailed results saved to: test_results.json\n")


if __name__ == "__main__":
    main()
