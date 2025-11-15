```markdown
# Color Analysis Questionnaire Logic

## Questions & Answer Options

### Q1: What is your natural hair color?
- Black
- Dark brown
- Light brown
- Blonde (golden/warm)
- Blonde (ash/cool)
- Red/Auburn
- Gray/White

### Q2: How would you describe your skin tone?
- Very fair (burns easily, rarely tans)
- Fair (burns sometimes, tans gradually)
- Light-medium (tans easily, rarely burns)
- Medium/Olive
- Tan/Caramel
- Deep/Rich brown
- Very deep/Dark brown

### Q3: What is your eye color?
- Light blue
- Blue-gray/Steel blue
- Green
- Hazel (green-brown)
- Light brown/Amber
- Dark brown
- Black

### Q4: Look at the veins on your wrist in natural light - what color are they?
- Blue/Purple (cool undertone indicator)
- Green (warm undertone indicator)
- Blue-green mix (neutral undertone indicator)
- Can't tell

### Q5: Which metals look best on you?
- Silver jewelry
- Gold jewelry
- Both look good
- Not sure

### Q6: Which colors do you wear most often?
(Multi-select, max 5)
- Black, Navy, Charcoal
- Brown, Beige, Camel
- White, Cream, Ivory
- Bright colors (red, royal blue, emerald)
- Muted colors (dusty rose, sage, burgundy)
- Pastels (baby blue, soft pink, lavender)
- Earth tones (rust, olive, terracotta)

### Q7: Which colors do you avoid or feel don't suit you?
(Multi-select, max 5)
- Same options as Q6

### Q8: When you wear certain colors, people say you look:
- Vibrant and glowing
- Washed out or tired
- It depends on the color
- No one comments

## Analysis Logic

### Step 1: Determine Undertone
**Warm indicators:**
- Green veins
- Gold jewelry preference
- Golden/warm blonde, red/auburn hair
- Wears earth tones, browns, warm colors

**Cool indicators:**
- Blue/purple veins
- Silver jewelry preference
- Ash blonde, black hair
- Wears blues, grays, jewel tones

**Neutral indicators:**
- Blue-green veins
- Both metals work
- Mix of warm/cool preferences

### Step 2: Determine Contrast Level
**High contrast:**
- Very fair skin + dark hair
- Deep skin + very dark hair
- Wears black, white, bright colors

**Medium contrast:**
- Most combinations
- Mix of bright and muted colors

**Low contrast:**
- Fair skin + blonde/light hair
- Medium/deep skin + brown/medium hair
- Prefers muted, soft colors

### Step 3: Map to Season

**SPRING (Warm + Bright)**
- Warm undertone
- Medium-high contrast
- Golden blonde, red, or light brown hair
- Prefers bright warm colors
- **Colors:** Coral, peach, bright yellow, warm pink, turquoise, warm green

**SUMMER (Cool + Soft)**
- Cool undertone
- Low-medium contrast
- Ash blonde, light brown, gray hair
- Prefers muted, soft colors
- **Colors:** Soft pink, lavender, powder blue, soft gray, mauve, cocoa

**AUTUMN (Warm + Muted)**
- Warm undertone
- Medium-low contrast
- Red, auburn, brown hair
- Prefers earth tones, muted warm colors
- **Colors:** Rust, olive, terracotta, warm brown, burnt orange, deep teal

**WINTER (Cool + Bright)**
- Cool undertone
- High contrast
- Black, dark brown, or white/gray hair
- Prefers bold, jewel tones, black/white
- **Colors:** True red, royal blue, emerald, pure white, black, magenta

### Step 4: Generate Palette

For each season, provide:
- **Core neutrals** (3-4 colors): Base wardrobe colors
- **Accent colors** (4-6 colors): Statement pieces
- **Avoid colors** (3-4 colors): What washes them out

### Step 5: MG Product Mapping

Tag MG products with:
- Primary color
- Temperature: Warm/Cool/Neutral
- Intensity: Bright/Muted/Deep
- Season compatibility: Spring/Summer/Autumn/Winter

Match user's season → Show compatible products

## Email Output Format

**Subject:** Your Personal Color Palette - [Season Name]

**Body:**
"Hi [Name],

Based on your responses, you're a **[SEASON]** - here's what that means for you:

**Your Best Colors:**
[Visual color swatches]
- [Core neutrals list]
- [Accent colors list]

**Why these work for you:**
[Brief explanation of their undertone + contrast]

**Colors to avoid:**
[List with brief why]

**Your Maison Guida Recommendations:**
[3-5 product images with links in their palette]

**Want a deeper analysis?**
Upload your photo for personalized styling advice and see exactly which shades within your palette are most flattering.
[Upload Photo Button/Link]

Ciao,
Maison Guida"

```

This gives you enough logic to build a working system. The questionnaire → season mapping isn't perfect (a photo would be better) but it's good enough to provide real value and capture emails.

Want to refine any part of this?
