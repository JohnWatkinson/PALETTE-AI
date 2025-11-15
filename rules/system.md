# Palette Color Analysis System

## Philosophy

This system is based on established color theory from the Bauhaus (Johannes Itten), refined by Suzanne Caygill and modernized for the 12-season method. It's not proprietary bullshit - it's color science.

## How It Works

### Three Core Dimensions

Every person's coloring can be analyzed across three axes:

1. **Undertone (Temperature)**: Warm, Cool, or Neutral
   - Based on skin's underlying pigmentation
   - Determined by hemoglobin show-through and melanin type

2. **Value (Depth)**: Light, Medium, or Dark
   - Overall lightness/darkness of hair, skin, eyes combined
   - Creates contrast level

3. **Chroma (Intensity)**: Bright/Clear, Muted/Soft, or Deep/Rich
   - How saturated vs. grayed the colors appear
   - Relates to skin clarity and color intensity

### 12 Seasons Breakdown

#### SPRING (Warm + Bright/Light)
- **Bright Spring**: Warm + Very Bright (high chroma)
- **True Spring**: Warm + Moderately Bright
- **Light Spring**: Warm + Light (low contrast)

#### SUMMER (Cool + Soft/Light)
- **Light Summer**: Cool + Very Light (low contrast)
- **True Summer**: Cool + Moderately Soft
- **Soft Summer**: Cool + Very Muted (lowest chroma)

#### AUTUMN (Warm + Muted/Deep)
- **Soft Autumn**: Warm + Very Muted
- **True Autumn**: Warm + Moderately Deep
- **Dark Autumn**: Warm + Very Deep (high contrast)

#### WINTER (Cool + Bright/Deep)
- **Dark Winter**: Cool + Very Deep (highest contrast)
- **True Winter**: Cool + Moderately Bright
- **Bright Winter**: Cool + Very Bright (high chroma)

## Decision Flow

```
1. UNDERTONE ANALYSIS
   ↓
   Warm / Cool / Neutral
   ↓
2. VALUE ANALYSIS
   ↓
   Light / Medium / Deep
   ↓
3. CHROMA ANALYSIS
   ↓
   Bright / Muted / Deep
   ↓
4. SEASON MAPPING
   ↓
   1 of 12 Seasons
```

## Signal-Based Scoring

Rather than rigid rules, we use weighted signals:
- Each answer provides evidence for certain characteristics
- Signals accumulate across questions
- Final determination uses highest-scoring combination
- Handles ambiguity and edge cases naturally

## AI Enhancement

Basic algorithm handles 90% of cases. AI adds:
- **Personalized explanations** of why the season fits
- **Edge case resolution** when signals are balanced
- **Conversational tone** that feels less robotic
- **Photo analysis** (Phase 5) for refinement

## Why This Works for MG

1. **Email capture**: Value exchange for palette
2. **Product recommendations**: Maps MG pieces to seasons
3. **Differentiation**: Most apps do 4 seasons, we do 12
4. **Accuracy**: Signal-based > rigid rules
5. **Scalability**: Can refine rules without touching code
