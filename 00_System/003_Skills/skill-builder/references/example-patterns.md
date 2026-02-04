# Example Skill Patterns

This reference provides annotated examples of different skill types, showing the reasoning behind design decisions.

## Table of Contents

1. [Workflow-Based Skill: PDF Processor](#workflow-based-skill-pdf-processor)
2. [Task-Based Skill: Image Editor](#task-based-skill-image-editor)
3. [Reference-Based Skill: Brand Guidelines](#reference-based-skill-brand-guidelines)
4. [Integration Skill: API Connector](#integration-skill-api-connector)

---

## Workflow-Based Skill: PDF Processor

This pattern works best when tasks follow predictable, sequential steps.

### Example SKILL.md

```markdown
---
name: pdf-processor
description: Process PDF files including merging, splitting, rotation, text extraction, and form filling. Use when the user asks to: combine PDFs, split PDF pages, rotate PDF pages, extract text from PDFs, fill PDF forms, or perform any PDF manipulation task.
---

# PDF Processor

## Overview

Process PDF files through consistent, reliable workflows.

## Workflow Decision Tree

**What does the user want to do?**

| User Request | Workflow |
|-------------|----------|
| Combine multiple PDFs | → Merge Workflow |
| Split PDF into pages | → Split Workflow |
| Rotate pages | → Rotation Workflow |
| Extract text | → Extraction Workflow |
| Fill form fields | → Form Workflow |

## Merge Workflow

1. Collect all input PDF paths
2. Validate each file exists and is readable
3. Run merge script
4. Verify output page count matches sum of inputs

```bash
python scripts/merge_pdfs.py output.pdf input1.pdf input2.pdf ...
```

## Rotation Workflow

1. Confirm rotation angle (90, 180, 270 degrees)
2. Confirm which pages (all, or specific range)
3. Run rotation script

```bash
python scripts/rotate_pdf.py input.pdf output.pdf --degrees 90 --pages all
```

## Form Workflow

For fillable PDF forms, see [references/form_filling.md](references/form_filling.md).
```

### Design Notes

**Why workflow-based works here:** PDF operations are highly procedural. Each task has specific steps that must happen in order. A workflow structure maps naturally to how the operations actually execute.

**Why the decision tree:** Users describe tasks in many ways ("merge these files", "combine into one PDF", "put these together"). The decision tree helps Claude map varied requests to the right workflow.

**Why scripts:** PDF manipulation code is error-prone and repetitive. Pre-tested scripts ensure reliability.

---

## Task-Based Skill: Image Editor

This pattern works best when a skill provides multiple independent capabilities.

### Example SKILL.md

```markdown
---
name: image-editor
description: Edit and manipulate images including resizing, cropping, rotation, format conversion, and filters. Use when the user asks to: resize images, crop images, rotate or flip images, convert image formats, apply filters, adjust brightness/contrast, or perform any image editing task.
---

# Image Editor

## Overview

Edit images using Python's Pillow library. All operations preserve quality by default.

## Quick Start

```python
from PIL import Image
img = Image.open("input.jpg")
# Apply operations
img.save("output.jpg", quality=95)
```

## Format Conversion

Convert between formats by changing the output extension:

```python
img = Image.open("photo.png")
img.convert("RGB").save("photo.jpg", quality=95)  # PNG→JPEG needs RGB mode
```

**Supported formats:** JPEG, PNG, WebP, GIF, BMP, TIFF

## Resizing

Resize while maintaining aspect ratio:

```python
img.thumbnail((800, 600))  # Fits within 800x600, preserves ratio
```

Resize to exact dimensions (may distort):

```python
img = img.resize((800, 600))
```

## Rotation

```python
img = img.rotate(90, expand=True)  # expand=True prevents cropping
```

For flip: `img.transpose(Image.FLIP_LEFT_RIGHT)`

## Cropping

```python
# crop(left, top, right, bottom)
cropped = img.crop((100, 100, 500, 400))
```

## Filters and Adjustments

See [references/filters.md](references/filters.md) for:
- Brightness, contrast, sharpness adjustment
- Blur, sharpen, edge detection
- Color manipulation
```

### Design Notes

**Why task-based works here:** Image editing operations are largely independent. Users ask for specific operations, not sequential workflows. Organizing by task makes it easy to find the right technique.

**Why inline code instead of scripts:** Image operations are simple enough that inline code is clearer than external scripts. Users often chain multiple operations, which inline code supports naturally.

**Why the Quick Start section:** Provides immediate utility for simple cases, with details available for specific needs.

---

## Reference-Based Skill: Brand Guidelines

This pattern works best for standards, specifications, and guidelines.

### Example SKILL.md

```markdown
---
name: acme-brand
description: Apply ACME Corp brand standards to documents, presentations, and graphics. Use when creating content for ACME, applying ACME branding, checking brand compliance, or when the user mentions ACME brand, style guide, or corporate identity.
---

# ACME Brand Guidelines

## Overview

All ACME content must follow these brand standards for consistency.

## Core Colors

| Color | Hex | Usage |
|-------|-----|-------|
| ACME Blue | #0052CC | Primary, headers, CTAs |
| ACME Gray | #42526E | Body text |
| ACME Light | #F4F5F7 | Backgrounds |
| Accent Green | #00875A | Success states only |

**Never use:** Gradients, drop shadows, or colors outside this palette.

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Headings | Inter | 24-48px | Bold |
| Body | Inter | 16px | Regular |
| Captions | Inter | 14px | Regular |

Line height: 1.5 for body text, 1.2 for headings.

## Logo Usage

The ACME logo is in `assets/acme-logo.svg`.

**Rules:**
- Minimum size: 24px height
- Clear space: 1x logo height on all sides
- Only use on white or ACME Light backgrounds
- Never rotate, stretch, or modify

## Voice and Tone

- **Clear:** Short sentences, simple words, no jargon
- **Confident:** Direct statements, avoid hedging
- **Helpful:** Focus on user benefit, not features

See [references/writing-style.md](references/writing-style.md) for detailed examples.
```

### Design Notes

**Why reference-based works here:** Brand guidelines are specifications to consult, not workflows to follow. Information needs to be findable and authoritative.

**Why tables:** Brand specifications are naturally tabular (color + hex + usage). Tables make lookup fast and prevent ambiguity.

**Why assets:** Brand assets (logos, templates) must be exact files, not recreated each time. Including them ensures consistency.

---

## Integration Skill: API Connector

This pattern works for skills that connect to external services.

### Example SKILL.md

```markdown
---
name: weather-api
description: Retrieve weather data from OpenWeatherMap API. Use when the user asks about weather conditions, forecasts, temperature, or climate data for any location.
---

# Weather API Integration

## Overview

Fetch current weather and forecasts using the OpenWeatherMap API.

## Authentication

Requires API key in environment variable:

```bash
export OPENWEATHER_API_KEY="your_key_here"
```

## Current Weather

```python
import os
import requests

def get_weather(city: str) -> dict:
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
```

**Response includes:**
- `main.temp`: Temperature in Celsius
- `main.humidity`: Humidity percentage
- `weather[0].description`: Conditions description
- `wind.speed`: Wind speed in m/s

## Forecast

For multi-day forecasts, use the forecast endpoint. See [references/forecast-api.md](references/forecast-api.md).

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Check OPENWEATHER_API_KEY |
| 404 | City not found | Try alternative city name |
| 429 | Rate limited | Wait 60 seconds, retry |

## Rate Limits

Free tier: 60 calls/minute, 1M calls/month.

For high-volume needs, see the paid tier options.
```

### Design Notes

**Why inline code for simple calls:** The API call is straightforward enough that inline code is clearer than a script. It shows exactly what's happening.

**Why explicit error table:** API integrations fail in predictable ways. Documenting errors upfront helps Claude handle them gracefully.

**Why authentication guidance:** API keys are a common pain point. Being explicit about where the key comes from prevents confusion.

---

## Combining Patterns

Complex skills often combine patterns. For example, a data analysis skill might:

1. **Task-based** organization for different analysis types (statistics, visualization, anomaly detection)
2. **Workflow-based** sections for complex multi-step analyses
3. **Reference-based** documentation for data schemas

The key is choosing the pattern that best fits each section's purpose, not forcing one pattern throughout.

### Example Mixed-Pattern Structure

```markdown
# Data Analyzer

## Quick Start (Task-based)
[Simple examples for common tasks]

## Analysis Types (Task-based)
### Descriptive Statistics
### Visualization
### Anomaly Detection

## Complex Analysis Workflow (Workflow-based)
1. Data loading
2. Cleaning
3. Analysis
4. Reporting

## Data Schema Reference (Reference-based)
[Table schemas, field definitions]
```

This structure lets users find simple answers quickly (task-based), follow complex procedures reliably (workflow-based), and look up detailed specifications (reference-based).
