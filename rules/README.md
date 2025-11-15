# Palette Color Analysis Rules

This directory contains the complete rule system for the color season analysis.

## File Structure

```
rules/
├── SYSTEM.md              # Philosophy and overview
├── seasons.yaml           # 12 season definitions with color palettes (hex codes)
├── questionnaire.yaml     # Questions with signal weights
├── mapping-rules.yaml     # Logic to convert signals → seasons
└── README.md             # This file
```

## How It Works

### 1. User Answers Questionnaire

Questions from `questionnaire.yaml` are presented to the user.
Each answer provides **weighted signals** for:
- **Undertone**: warm, cool, neutral
- **Value**: light, medium, deep
- **Chroma**: bright, muted, soft, rich
- **Contrast**: high, medium, low

Example:
```yaml
- id: "red_auburn"
  label: "Red/Auburn"
  signals:
    undertone: { warm: 4 }  # Strong warm signal
    chroma: { rich: 2 }     # Moderate rich signal
```

### 2. Signals Accumulate

As user answers questions, signals are summed:

```
undertone_warm: 12
undertone_cool: 3
value_light: 8
value_deep: 2
chroma_bright: 6
chroma_muted: 3
```

### 3. Characteristics Determined

Using thresholds from `mapping-rules.yaml`:

```
Dominant Undertone: Warm (12 > 8 threshold)
Dominant Value: Light (8 > 6 threshold)
Dominant Chroma: Bright (6 > 5 threshold)
```

### 4. Season Mapped

Combination of characteristics maps to specific season:

```
warm + light + bright = Light Spring
```

### 5. Confidence Calculated

Based on:
- How strong the signals are
- Whether there are conflicts
- Edge case handling

Result: `Light Spring (85% confidence)`

### 6. AI Enhancement (Optional)

If confidence < 70% OR user wants personalization:
- Generate natural language explanation
- Resolve ambiguous cases
- Create personalized color story
- Suggest MG products

## Implementation Guide

### Backend (Python/Node)

```python
# Pseudocode

def analyze_questionnaire(responses):
    # 1. Load questionnaire rules
    questions = load_yaml('questionnaire.yaml')

    # 2. Accumulate signals
    signals = {}
    for response in responses:
        question = questions[response.question_id]
        option = question.options[response.answer_id]

        for signal_type, values in option.signals.items():
            for key, weight in values.items():
                signals[f"{signal_type}_{key}"] += weight

    # 3. Determine characteristics
    rules = load_yaml('mapping-rules.yaml')

    undertone = determine_undertone(signals, rules)
    value = determine_value(signals, rules)
    chroma = determine_chroma(signals, rules)

    # 4. Map to season
    season = find_matching_season(undertone, value, chroma, rules)
    confidence = calculate_confidence(signals, season, rules)

    # 5. Get palette
    seasons = load_yaml('seasons.yaml')
    palette = seasons[season]

    # 6. Optional AI enhancement
    if confidence < 70 or user_wants_personalization:
        explanation = ai_explain(season, signals, user_responses)
    else:
        explanation = template_explanation(season)

    return {
        'season': season,
        'confidence': confidence,
        'palette': palette,
        'explanation': explanation
    }
```

### AI Integration

```python
def ai_explain(season, signals, responses):
    prompt = f"""
    The user has been analyzed as a {season}.

    Their signals were:
    {json.dumps(signals)}

    Their questionnaire responses:
    {json.dumps(responses)}

    Write a friendly, personal 2-3 paragraph explanation of:
    1. Why they are this season
    2. What this means for their coloring
    3. How to use their palette

    Tone: Warm, conversational, not technical.
    No fluff, direct and helpful.
    """

    return llm_call(prompt, max_tokens=200)
```

## Updating Rules

### Adding New Questions

Edit `questionnaire.yaml`:

```yaml
q9_new_question:
  id: "q9"
  question: "Your question here?"
  type: "single_choice"
  options:
    - id: "option1"
      label: "Option 1"
      signals:
        undertone: { warm: 2 }
```

### Adjusting Signal Weights

If you find the algorithm is miscategorizing:

1. Check which signals are accumulating incorrectly
2. Adjust weights in `questionnaire.yaml`
3. Test with known examples
4. Iterate

### Tweaking Thresholds

Edit `mapping-rules.yaml`:

```yaml
undertone_rules:
  warm_threshold: 8    # Increase if too many neutrals
  cool_threshold: 8
  neutral_range: [5, 7]
```

### Adding Confidence Modifiers

Make seasons more distinct:

```yaml
true_autumn:
  conditions:
    undertone: "warm"
    chroma: "rich"
  confidence_modifiers:
    - if_has: ["red_auburn_hair"]
      boost: 0.20  # Increase boost
```

## Season Quick Reference

| Season | Undertone | Value | Chroma | Examples |
|--------|-----------|-------|--------|----------|
| Bright Spring | Warm | Medium | Bright | Coral, turquoise, golden yellow |
| True Spring | Warm | Medium | Clear | Peach, warm aqua, buttercup |
| Light Spring | Warm | Light | Soft | Light peach, mint, cream |
| Light Summer | Cool | Light | Soft | Powder blue, soft rose, lavender |
| True Summer | Cool | Medium | Muted | Dusty rose, soft teal, mauve |
| Soft Summer | Cool | Medium | Very Muted | Dusty lavender, sage, taupe |
| Soft Autumn | Warm | Medium | Muted | Soft coral, sage, terracotta |
| True Autumn | Warm | Medium | Rich | Rust, forest green, burnt orange |
| Dark Autumn | Warm | Deep | Rich | Deep rust, hunter green, bronze |
| Dark Winter | Cool | Deep | Bright | True red, emerald, royal blue |
| True Winter | Cool | Med-Deep | Bright | True red, icy blue, magenta |
| Bright Winter | Cool | Medium | Very Bright | Shocking pink, electric blue, lime |

## MG Product Tagging

Tag each MG product with:

```yaml
product_id: "MG0042-BLK-M"
color_analysis:
  primary_color: "#000000"
  undertone: "cool"
  intensity: "deep"
  seasons: ["dark_winter", "true_winter", "bright_winter"]
```

Then filter products by user's season.

## Testing

Create test cases:

```python
test_cases = [
    {
        'name': 'Classic Spring',
        'responses': {
            'q1': 'golden_blonde',
            'q2': 'fair',
            'q4': 'green',
            'q5': 'gold',
            # ...
        },
        'expected_season': 'true_spring',
        'min_confidence': 75
    }
]
```

Run through algorithm, verify results.

## Future Enhancements

1. **Photo Analysis** (Phase 5)
   - Upload photo
   - AI analyzes actual coloring
   - Refines questionnaire result

2. **Sub-season Variations**
   - Split 12 seasons into 24 or 48 sub-types
   - More nuanced palettes

3. **Seasonal Blends**
   - Some people are "Spring-Autumn blend"
   - Show primary + secondary season

4. **Dynamic Palettes**
   - Generate custom hex codes based on exact coloring
   - Not just pre-defined palettes

5. **Makeup Integration**
   - Foundation shade recommendations
   - Lip/blush colors
   - Hair color suggestions

## Philosophy

> "The seasons are metaphors for color harmony in nature. Everyone fits somewhere in this system because humans ARE nature. The certification industry gatekeeps this knowledge, but the core logic is just color theory - warm/cool, light/dark, bright/muted. That's it."

Keep the rules transparent, updateable, and grounded in actual color science - not marketing woo.
