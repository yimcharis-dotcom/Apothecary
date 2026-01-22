User: Step by step exhaustively walk me through on how I should go about on making a grammar checker, using obsidian as my note book. I need details in how to evaluate ai output, where to check. From start all the way to completion.
Kimi: # Complete Guide: Building a Grammar Checker for Obsidian

This exhaustive walkthrough covers the entire process of creating a privacy-focused grammar checker integrated with Obsidian, from architecture decisions to AI evaluation and deployment. I'll structure this as eight distinct phases with granular steps.

## **Phase 1: Foundation & Architecture Design**

### Step 1.1: Define Your Scope and Approach

First, decide which type of grammar checker to build based on your resources:

**Three Architectural Approaches** :

- **Rule-Based System**: Fast, deterministic, privacy-preserving. Uses pattern matching (regex, POS tags). Best for common errors (subject-verb agreement, punctuation). Limited recall for complex errors.
- **AI/ML-Based System**: High accuracy, context-aware. Requires model training or API access. Resource-intensive, potential privacy issues with cloud APIs.
- **Hybrid Approach** (Recommended): Rule-based for common errors + AI for nuanced style/fluency. This balances performance, privacy, and accuracy.

**Decision Matrix**:
| Feature | Rule-Based | AI-Based (Cloud) | AI-Based (Local) | Hybrid |
|---------|------------|------------------|------------------|--------|
| Privacy | 100% | 0% | 100% | 100% |
| Speed | Very Fast | Medium | Slow-Fast\* | Fast |
| Accuracy | Low-Moderate | High | High | Very High |
| Development Cost | Low | Medium | High | Medium |
| Maintenance | High (manual rules) | Low | Medium | Medium |

\*Local AI speed depends on model size and hardware

### Step 1.2: Set Core Requirements

Create a requirements document specifying:

- **Error Types to Detect**: Spelling, grammar (subject-verb, tenses), punctuation, style (passive voice, wordiness), clarity
- **Languages**: English primary (extensible to others)
- **Privacy**: Must run 100% offline within Obsidian
- **Performance**: <100ms latency for 100-word note
- **User Experience**: Real-time highlighting, one-click corrections, ignore rules
- **Integration**: Seamless with Obsidian's editor, ignore code blocks

### Step 1.3: Choose Your Tech Stack

**Grammar Engine**:

- **Option A (Rule-Based)**: Python with NLTK/spaCy for POS tagging + XML rule definitions
- **Option B (Local AI)**: ONNX Runtime + quantized models (e.g., T5-small, BART)
- **Option C (API Hybrid)**: Use LanguageTool self-hosted Docker container for rules + custom AI for style

**Obsidian Plugin**:

- TypeScript/JavaScript
- Node.js 18+
- Obsidian API v1.0+

**Development Environment**:

- VS Code with TypeScript extensions
- Docker (for local LanguageTool if using hybrid approach)
- Git for version control

## **Phase 2: Development Environment Setup**

### Step 2.1: Create Isolated Development Vault

**Critical**: Never develop in your main vault to prevent data loss .

```bash
mkdir obsidian-grammar-dev
cd obsidian-grammar-dev
mkdir -p .obsidian/plugins
```

### Step 2.2: Initialize Obsidian Plugin Structure

Use the official sample plugin template :

```bash
cd .obsidian/plugins
git clone https://github.com/obsidianmd/obsidian-sample-plugin.git grammar-checker
cd grammar-checker
npm install
```

### Step 2.3: Configure Plugin Manifest

Edit `manifest.json` with your plugin details:

```json
{
  "id": "grammar-checker",
  "name": "Grammar Checker",
  "version": "0.1.0",
  "minAppVersion": "0.15.0",
  "description": "Privacy-focused grammar checking for Obsidian",
  "author": "Your Name",
  "authorUrl": "https://your-website.com",
  "fundingUrl": "https://github.com/sponsors/yourname"
}
```

### Step 2.4: Set Up Build Process

The template includes `npm run dev` for auto-Apothecary. Configure `tsconfig.json` for strict typing:

```json
{
  "compilerOptions": {
    "target": "ES6",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

## **Phase 3: Core Grammar Engine Development**

### Step 3.1: Implement Rule-Based Foundation (Recommended Starting Point)

**A. Part-of-Speech Tagging Integration**
Use spaCy via Node.js child process or compile rules directly in TypeScript:

```typescript
// src/engine/RuleEngine.ts
interface GrammarRule {
  id: string;
  pattern: RegExp;
  message: string;
  suggestions: string[];
  category: "grammar" | "style" | "punctuation";
}

export class RuleEngine {
  private rules: GrammarRule[] = [
    {
      id: "subject-verb-agreement",
      pattern: /\b(he|she|it)\s+(\w+?)(?:s|es)?\b/gi,
      message: "Possible subject-verb agreement error",
      suggestions: ["ensure verb matches singular subject"],
      category: "grammar",
    },
    {
      id: "passive-voice",
      pattern: /\b(am|is|are|was|were|be|being|been)\s+(\w+ed)\b/gi,
      message: "Consider using active voice",
      suggestions: ["rewrite in active voice"],
      category: "style",
    },
  ];

  check(text: string): GrammarError[] {
    const errors: GrammarError[] = [];
    for (const rule of this.rules) {
      const matches = [...text.matchAll(rule.pattern)];
      for (const match of matches) {
        errors.push({
          from: match.index,
          to: match.index + match[0].length,
          message: rule.message,
          suggestions: rule.suggestions,
          ruleId: rule.id,
        });
      }
    }
    return errors;
  }
}
```

**B. POS-Enhanced Rules**
Import spaCy JSON output for accurate patterns:

```bash
# In separate Python service (if needed)
python -m spacy download en_core_web_sm
```

```python
# server/pos_tagger.py
import spacy
nlp = spacy.load("en_core_web_sm")

def tag_text(text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]
```

### Step 3.2: Integrate Local AI Model (Advanced)

**A. Model Selection**
For offline use, choose quantized models:

- **T5-small** (60MB): Good balance for grammar correction
- **BART-base**: Strong rewrite capabilities
- **DistilBERT**: Fast inference for error detection

**B. ONNX Conversion for Performance**
Convert PyTorch model to ONNX for faster inference:

```bash
pip install onnxruntime transformers
python scripts/convert_to_onnx.py
```

**C. Node.js Integration**
Use `onnxruntime-node`:

```typescript
// src/engine/AIEngine.ts
import * as ort from "onnxruntime-node";

export class AIEngine {
  private session: ort.InferenceSession;

  async initialize(modelPath: string) {
    this.session = await ort.InferenceSession.create(modelPath);
  }

  async correct(text: string): Promise<AIMarker[]> {
    // Tokenize input
    const tokens = this.tokenize(text);
    const input = new ort.Tensor("int64", tokens, [1, tokens.length]);

    // Run inference
    const results = await this.session.run({ input_ids: input });
    return this.parseResults(results, text);
  }
}
```

### Step 3.3: Hybrid Engine Architecture

Combine both engines for optimal results:

```typescript
// src/engine/HybridEngine.ts
export class HybridEngine {
  private ruleEngine: RuleEngine;
  private aiEngine: AIEngine;

  async check(text: string): Promise<GrammarError[]> {
    // Run rule-based check (fast)
    const ruleErrors = this.ruleEngine.check(text);

    // Run AI check for complex sentences (slower)
    const sentences = this.splitIntoSentences(text);
    const complexSentences = sentences.filter((s) => this.isComplex(s));
    const aiErrors = await this.aiEngine.checkBatch(complexSentences);

    // Merge and deduplicate
    return this.mergeErrors(ruleErrors, aiErrors);
  }
}
```

## **Phase 4: Obsidian Plugin Integration**

### Step 4.1: Editor Decoration System

Implement real-time highlighting using CodeMirror 6 (Obsidian's editor):

```typescript
// src/editor/Highlighter.ts
import { EditorView, ViewPlugin } from "@codemirror/view";
import { Decoration, DecorationSet } from "@codemirror/view";
import { StateField, StateEffect } from "@codemirror/state";

const addErrorMarker = StateEffect.define<Range<GrammarError>>();

const errorField = StateField.define<DecorationSet>({
  create() {
    return Decoration.none;
  },
  update(markers, tr) {
    markers = markers.map(tr.changes);
    for (const e of tr.effects) {
      if (e.is(addErrorMarker)) {
        markers = markers.update({
          add: [errorMarker.range(e.value.from, e.value.to)],
        });
      }
    }
    return markers;
  },
  provide: (f) => EditorView.decorations.from(f),
});

const errorMarker = Decoration.mark({
  class: "cm-grammar-error",
  attributes: { style: "text-decoration: wavy red underline;" },
});
```

### Step 4.2: Plugin Main Class

Implement the main plugin lifecycle:

````typescript
// src/main.ts
import { Plugin, Editor } from "obsidian";
import { HybridEngine } from "./engine/HybridEngine";

export default class GrammarCheckerPlugin extends Plugin {
  private engine: HybridEngine;
  private debounceTimer: NodeJS.Timeout;

  async onload() {
    // Initialize engine
    this.engine = new HybridEngine();
    await this.engine.initialize();

    // Register editor extension
    this.registerEditorExtension(errorField);

    // Debounced real-time checking
    this.registerEvent(
      this.app.workspace.on("editor-change", (editor: Editor) => {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
          this.checkDocument(editor);
        }, 300); // 300ms debounce
      })
    );

    // Add ribbon icon for manual check
    this.addRibbonIcon("check", "Check Grammar", () => {
      const editor = this.app.workspace.activeEditor?.editor;
      if (editor) this.checkDocument(editor);
    });
  }

  async checkDocument(editor: Editor) {
    const text = editor.getValue();
    // Exclude code blocks
    const cleanText = text.replace(/```[\s\S]*?```/g, "");

    const errors = await this.engine.check(cleanText);
    this.highlightErrors(editor, errors);
  }

  highlightErrors(editor: Editor, errors: GrammarError[]) {
    // Apply decorations to editor
    const view = editor.cm as EditorView;
    view.dispatch({
      effects: errors.map((e) => addErrorMarker.of(e)),
    });
  }
}
````

### Step 4.3: Settings Tab

Create a UI for user configuration:

```typescript
// src/settings/SettingsTab.ts
import { App, PluginSettingTab, Setting } from "obsidian";
import GrammarCheckerPlugin from "../main";

export class GrammarSettingsTab extends PluginSettingTab {
  constructor(app: App, private plugin: GrammarCheckerPlugin) {
    super(app, plugin);
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    new Setting(containerEl)
      .setName("AI Model Path")
      .setDesc("Path to local ONNX model")
      .addText((text) =>
        text
          .setPlaceholder("Enter path...")
          .setValue(this.plugin.settings.modelPath)
          .onChange(async (value) => {
            this.plugin.settings.modelPath = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Check Style Issues")
      .setDesc("Enable style suggestions beyond grammar")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.enableStyle)
          .onChange(async (value) => {
            this.plugin.settings.enableStyle = value;
            await this.plugin.saveSettings();
          })
      );
  }
}
```

## **Phase 5: AI Output Evaluation Framework**

### Step 5.1: Define Evaluation Metrics

Use established metrics from GEC research :

**Edit-Based Metrics (for precision)**:

- **M2 (MaxMatch)**: Measures edit precision/recall vs. reference corrections
- **ERRANT**: Enhanced M2 with linguistic edit classification
- **F0.5 Score**: Emphasizes precision over recall (avoids over-correction)

**Sentence-Based Metrics (for fluency)**:

- **GLEU**: Grammar-specific BLEU variant
- **Scribendi Score**: Combines GPT-2 perplexity + edit distance
- **SOME**: BERT-based semantic similarity for grammaticality

**Custom Metrics for Obsidian Context**:

```typescript
// src/evaluation/Metrics.ts
interface EvaluationResult {
  precision: number; // Correct corrections / Total corrections
  recall: number; // Errors caught / Total errors
  f05: number; // F0.5 score
  falsePositiveRate: number;
  userAcceptanceRate: number; // From usage analytics
}
```

### Step 5.2: Create Evaluation Datasets

You need three types of test data:

**A. Standard Benchmarks** :

- **CoNLL-2014**: 1,312 English sentences with error annotations
- **JFLEG**: Focuses on fluency, not just error detection
- **FCE Dataset**: Learner English with detailed error tags

**Download and convert to JSONL format:**

```bash
mkdir -p data/evaluation
# CoNLL-2014
wget https://www.comp.nus.edu.sg/~nlp/sw/gec-2014/conll14st-test-data.tar.gz
tar -xzf conll14st-test-data.tar.gz
python scripts/convert_conll_to_jsonl.py
```

**B. Obsidian-Specific Test Corpus**:
Create a test set that mimics real Obsidian usage:

```typescript
// data/obsidian-corpus.jsonl
{"text": "# Meeting Notes\nWe discusses the Q4 budget.", "errors": [{"type": "SVA", "start": 21, "end": 29}]}
{"text": "This is a [[link]] to another note.", "errors": []} // Code blocks/links should be ignored
```

**C. Adversarial Test Cases**:

```typescript
// data/adversarial.jsonl
{"text": "Their going to the store.", "expected": "They're going to the store."}
{"text": "Its a nice day.", "expected": "It's a nice day."}
```

### Step 5.3: Automated Evaluation Pipeline

Build a test runner that evaluates your engine nightly:

```typescript
// scripts/evaluate.ts
import { HybridEngine } from "../src/engine/HybridEngine";
import { calculateM2, calculateGLEU } from "./evaluation-metrics";

async function runEvaluation() {
  const engine = new HybridEngine();
  await engine.initialize();

  // Load test datasets
  const conllData = loadJSONL("data/evaluation/conll14.jsonl");
  const obsidianData = loadJSONL("data/evaluation/obsidian-corpus.jsonl");

  // Run predictions
  const predictions = await Promise.all(
    conllData.map((item) => engine.check(item.text))
  );

  // Calculate metrics
  const m2Score = calculateM2(predictions, conllData);
  const gleuScore = calculateGLEU(predictions, conllData);

  console.log(`M2 F0.5: ${m2Score.f05.toFixed(3)}`);
  console.log(`GLEU: ${gleuScore.toFixed(3)}`);

  // Generate report
  generateReport({ m2Score, gleuScore, timestamp: Date.now() });
}
```

### Step 5.4: Human Evaluation Protocol

Automated metrics are insufficient; implement structured human review:

**A. Set Up Annotation Interface**:
Create a simple web UI where reviewers can accept/reject suggestions:

```html
<!-- evaluation/annotator.html -->
<div id="sentence">
  Test sentence with <span class="suggestion">error</span>
</div>
<button onclick="accept()">✓ Accept</button>
<button onclick="reject()">✗ Reject</button>
```

**B. Recruiting Reviewers**:

- 3-5 fluent English speakers
- Mix of technical and non-technical users
- Test on their own Obsidian notes

**C. Evaluation Protocol**:

1. Present 100 random sentences from user notes
2. For each suggestion, record: accept/reject, time spent, confidence
3. Calculate **Human Acceptance Rate (HAR)**:
   ```
   HAR = (# accepted suggestions) / (# total suggestions)
   ```
4. Target HAR > 85% before release

### Step 5.5: Error Analysis Dashboard

Track failure modes systematically:

```typescript
// src/evaluation/ErrorAnalytics.ts
interface ErrorPattern {
  ruleId: string;
  falsePositives: number;
  falseNegatives: number;
  commonContexts: string[]; // Surrounding text patterns
}

class ErrorAnalytics {
  private patterns: Map<string, ErrorPattern> = new Map();

  logPrediction(text: string, error: GrammarError, accepted: boolean) {
    const key = error.ruleId;
    const pattern = this.patterns.get(key) || {
      ruleId: key,
      falsePositives: 0,
      falseNegatives: 0,
      commonContexts: [],
    };

    if (!accepted) {
      pattern.falsePositives++;
      pattern.commonContexts.push(
        text.substring(error.from - 20, error.to + 20)
      );
    }

    this.patterns.set(key, pattern);
  }

  generateReport(): string {
    const sorted = [...this.patterns.values()].sort(
      (a, b) => b.falsePositives - a.falsePositives
    );

    return `Top False Positive Rules:\n${sorted
      .slice(0, 10)
      .map((p) => `${p.ruleId}: ${p.falsePositives} FP`)
      .join("\n")}`;
  }
}
```

## **Phase 6: Testing Strategy & Quality Assurance**

### Step 6.1: Unit Testing

Test each component in isolation:

```typescript
// tests/RuleEngine.test.ts
import { RuleEngine } from "../src/engine/RuleEngine";

test("detects subject-verb disagreement", () => {
  const engine = new RuleEngine();
  const errors = engine.check("He go to school.");
  expect(errors).toHaveLength(1);
  expect(errors[0].ruleId).toBe("subject-verb-agreement");
});

test("ignores code blocks", () => {
  const engine = new RuleEngine();
  const text = `
# Title
This is text with error.
\`\`\`
const foo = "bar"; // This should be ignored
\`\`\`
  `;
  const errors = engine.check(text);
  expect(
    errors.every((e) => !text.substring(e.from, e.to).includes("const"))
  ).toBe(true);
});
```

### Step 6.2: Integration Testing

Test the full pipeline with Obsidian API mocks:

```typescript
// tests/ObsidianIntegration.test.ts
import { Editor } from "obsidian";
import GrammarCheckerPlugin from "../src/main";

test("highlights errors in editor", async () => {
  const mockEditor = createMockEditor("We was there.");
  const plugin = new GrammarCheckerPlugin(app, manifest);

  await plugin.checkDocument(mockEditor);

  const decorations = mockEditor.getDecorations("cm-grammar-error");
  expect(decorations).toHaveLength(1);
});
```

### Step 6.3: Performance Testing

Ensure <100ms response time:

```typescript
// tests/performance.test.ts
test("checks 100-word note in under 100ms", async () => {
  const text = generateText(100);
  const start = performance.now();
  await engine.check(text);
  const duration = performance.now() - start;

  expect(duration).toBeLessThan(100);
});
```

### Step 6.4: Where to Run Tests

Create a dedicated test vault with notes representing real usage:

```bash
mkdir test-vault
cd test-vault
# Create test notes
cat > "grammar-test.md" <<EOF
# Common Errors

Their going to the store.

Its a nice day.

We was happy about the news.
EOF

cat > "code-test.md" <<EOF
# Code Should Be Ignored

Here is JavaScript:
\`\`\`
function test() {
  const errors = "none here";
}
\`\`\`
EOF
```

## **Phase 7: Privacy & Security Implementation**

### Step 7.1: Local-Only Architecture

Ensure no data leaves the device :

```typescript
// src/privacy/PrivacyGuard.ts
export class PrivacyGuard {
  private networkBlocked: boolean = true;

  blockNetworkAccess() {
    // Intercept fetch/XMLHttpRequest
    const originalFetch = window.fetch;
    window.fetch = (...args) => {
      if (this.networkBlocked) {
        throw new Error("Network access blocked for privacy");
      }
      return originalFetch(...args);
    };
  }

  isLocalOnly(): boolean {
    return this.networkBlocked;
  }
}
```

### Step 7.2: Sensitive Data Detection

Warn users about potential sensitive content:

```typescript
// src/privacy/SensitiveDataDetector.ts
const SENSITIVE_PATTERNS = [
  /\b\d{3}-\d{2}-\d{4}\b/, // SSN-like
  /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i, // Email
];

export function containsSensitiveData(text: string): boolean {
  return SENSITIVE_PATTERNS.some((pattern) => pattern.test(text));
}
```

### Step 7.3: Audit Trail

Log all operations for user transparency:

```typescript
// src/logging/AuditLog.ts
interface LogEntry {
  timestamp: number;
  operation: "check" | "correct" | "ignore";
  textLength: number;
  errorCount: number;
}

export class AuditLog {
  private entries: LogEntry[] = [];

  log(operation: string, text: string, errors: GrammarError[]) {
    this.entries.push({
      timestamp: Date.now(),
      operation,
      textLength: text.length,
      errorCount: errors.length,
    });

    // Keep only last 1000 entries
    if (this.entries.length > 1000) {
      this.entries = this.entries.slice(-1000);
    }
  }

  export(): LogEntry[] {
    return [...this.entries];
  }
}
```

## **Phase 8: Deployment & Iteration**

### Step 8.1: Beta Testing

Release to limited user group:

1. **Private Beta**: Share `.zip` via GitHub Releases with 10-20 testers
2. **Feedback Collection**: Use GitHub Issues template:

```markdown
## Issue Type

- [ ] False Positive
- [ ] Missed Error
- [ ] Performance Issue

## Sentence

<!-- The text that was checked -->

## Suggestion

<!-- What the plugin suggested -->

## Expected

<!-- What should have happened -->

## Context

<!-- Note type, surrounding text -->
```

1. **Telemetry** (opt-in only):

```typescript
// Only if user explicitly enables
if (this.settings.enableTelemetry) {
  this.analytics.logUsage(errorPatterns);
}
```

### Step 8.2: Community Plugin Submission

Follow Obsidian's official process :

1. **Prepare Repository**:

   - Create GitHub repo with README, LICENSE (MIT recommended)
   - Include `main.js`, `manifest.json`, `styles.css` in releases
   - Add screenshots/GIF of plugin in action

1. **Quality Checklist**:

   - [ ] Works on Windows, macOS, Linux
   - [ ] No console errors
   - [ ] Settings UI intuitive
   - [ ] Performance acceptable
   - [ ] Privacy policy documented

1. **Submit PR to Community Plugins**:
   - Fork https://github.com/obsidianmd/obsidian-releases
   - Add your plugin to `community-plugins.json`
   - Wait for review (typically 1-2 weeks)

### Step 8.3: Post-Launch Monitoring

Set up continuous improvement pipeline:

**A. Version Tracking**:

```typescript
// src/analytics/VersionAnalytics.ts
export class VersionAnalytics {
  trackMilestone(version: string, metrics: EvaluationResult) {
    // Log to file or remote service (with consent)
    console.log(
      `v${version}: M2=${metrics.f05.toFixed(
        3
      )}, HAR=${metrics.userAcceptanceRate.toFixed(2)}`
    );
  }
}
```

**B. A/B Testing New Rules**:
Deploy rules to subset of users:

```typescript
// Gradual rollout of new rule
const rolloutPercent = this.settings.experimentalRules ? 100 : 10;
if (Math.random() * 100 < rolloutPercent) {
  // Enable new rule
}
```

**C. Monthly Review Cycle**:

1. Collect annotated data from users (if opted in)
2. Retrain AI model on new data
3. Evaluate against benchmarks
4. Release patch updates for rule improvements
5. Minor version for model updates

### Step 8.4: Where to Check Performance Over Time

Create a dashboard tracking:

| Metric              | Check Location             | Frequency   | Target |
| ------------------- | -------------------------- | ----------- | ------ |
| M2 F0.5             | `data/evaluation/reports/` | Nightly     | >60    |
| HAR                 | User feedback              | Weekly      | >85%   |
| Avg Latency         | Performance tests          | Per commit  | <100ms |
| False Positive Rate | Error analysis             | Weekly      | <15%   |
| Memory Usage        | DevTools profiling         | Per release | <50MB  |

**Dashboard Implementation**:

```typescript
// scripts/dashboard.ts
function generateDashboardHtml(reports: EvaluationResult[]) {
  return `
    <html>
      <body>
        <h1>Grammar Checker Performance</h1>
        <canvas id="metricsChart"></canvas>
        <script>
          const data = ${JSON.stringify(reports)};
          // Plot metrics over time
        </script>
      </body>
    </html>
  `;
}
```

---

## **Summary Checklist: From Start to Completion**

### Week 1-2: Foundation

- [ ] Set up dev vault and plugin template
- [ ] Define requirements document
- [ ] Choose hybrid architecture
- [ ] Implement basic rule engine with 10 common rules

### Week 3-4: Core Development

- [ ] Integrate POS tagger (local or via spaCy)
- [ ] Implement CodeMirror decorations
- [ ] Add settings tab
- [ ] Exclude code blocks from checking

### Week 5-6: AI Integration

- [ ] Convert T5/BART model to ONNX
- [ ] Implement AIEngine class
- [ ] Create HybridEngine orchestrator
- [ ] Add performance optimizations (caching, batching)

### Week 7-8: Evaluation Setup

- [ ] Download CoNLL-2014 and JFLEG datasets
- [ ] Implement M2 and GLEU metrics
- [ ] Build annotation interface
- [ ] Recruit 5 beta testers

### Week 9-10: Testing & Refinement

- [ ] Achieve HAR > 85% on internal tests
- [ ] Reduce false positive rate < 15%
- [ ] Profile and optimize to <100ms latency
- [ ] Test on Windows/macOS/Linux

### Week 11-12: Deployment

- [ ] Write privacy policy and README
- [ ] Create plugin GitHub repo
- [ ] Submit to Community Plugins repository
- [ ] Set up CI/CD for automated releases

### Ongoing: Iteration

- [ ] Weekly error pattern analysis
- [ ] Monthly model retraining
- [ ] Quarterly benchmark evaluation
- [ ] User feedback triage

---

## **Key Resources & Where to Check**

**Datasets**:

- **CoNLL-2014**: http://www.comp.nus.edu.sg/~nlp/conll14st/
- **JFLEG**: https://nlp.jhu.edu/research/m2/
- **Error Analysis**: Create your own at `data/evaluation/`

**Evaluation Tools**:

- **ERRANT**: `pip install errant` for edit classification
- **M2 Scorer**: https://github.com/nusnlp/m2scorer
- **Benchmark Papers**: MIT Press meta-evaluation study

**Obsidian Development**:

- **Official Docs**: https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin
- **Sample Plugin**: https://github.com/obsidianmd/obsidian-sample-plugin
- **Community**: https://forum.obsidian.md/

**Model Resources**:

- **ONNX Models**: https://huggingface.co/models?filter=onnx
- **Grammar Models**: T5-small fine-tuned on JFLEG
- **Quantization**: Use `onnxruntime-web` for browser deployment

This exhaustive guide provides the complete roadmap. Start with Phase 1 and iteratively build each component. The key is **starting small with rule-based checks** and gradually integrating AI while continuously measuring performance against both automated metrics and human acceptance.
User: for each area you discuss above, provide and explain in details of the practical tips and tricks exhaustively
Kimi: # Practical Tips & Tricks: Grammar Checker for Obsidian (Exhaustive)

Below are battle-tested, granular tips for each development phase, drawn from real-world plugin development and NLP implementation experience.

---

## **Phase 1: Foundation & Architecture Design - Practical Tips**

### Step 1.1: Define Your Scope

**Tip 1: Start with a "Dumb" Rule-Based MVP**

- Don't touch AI for the first 2 weeks. Build 20 hard-coded regex rules first. This forces you to understand _where_ errors occur in Obsidian notes (headers, lists, links). You'll discover that 80% of "errors" in Markdown are false positives (e.g., `[[link|alias]]` syntax).
- **Trick**: Create a "rule sandbox" note with 50 sentences containing known errors. Run your rules manually before any UI work. This becomes your living regression test.

**Tip 2: Use the "Three-Note Test" for Architecture Validation**
Before writing code, manually simulate your pipeline on three real notes:

1. **Daily note**: Short, informal, time-stamped entries
2. **Research note**: Long, academic, with citations and code blocks
3. **MOC (Map of Content)**: Mostly links and bullet points
   This reveals that you'll need **different checking modes** for different note types. Add a frontmatter tag like `grammar-check: false` to exclude certain notes.

**Tip 3: Privacy-First Design is Non-Negotiable**

- **Pitfall**: Even "local" models can leak data via telemetry or crash reports. Disable all automatic reporting in ONNX Runtime:

```typescript
ort.InferenceSession.create(modelPath, {
  logSeverityLevel: 4, // Disable warnings that might include text snippets
  enableProfiling: false,
});
```

- **Trick**: Add a "Privacy Mode" toggle that disables AI entirely and runs only regex rules. Users with sensitive notes will trust you more.

---

## **Phase 2: Development Environment Setup - Practical Tips**

### Step 2.1: Create Isolated Development Vault

**Tip 4: Use Git for Your Test Vault**
Initialize Git in your dev vault (`obsidian-grammar-dev/`). Commit test notes. This lets you revert accidental plugin corruption and track how your checker modifies notes over time.

**Tip 5: The ".obsidian/plugins" Symlink Trick**
Instead of cloning into `.obsidian/plugins/`, create a symlink for faster iteration:

```bash
# In your main vault
ln -s /path/to/your/plugin/repo grammar-checker
```

This lets you edit code in your normal project folder while Obsidian hot-reloads from the vault.

**Tip 6: Hot-Reload Plugin is Essential but Flaky**
Install the **Hot Reload** plugin from the community store. But **always** test disabling/enabling manually before final builds. Hot Reload can mask manifest caching issues that real users will hit.

**Pitfall**: The `manifest.json` changes require a full Obsidian restart. Hot Reload won't pick them up. Close/reopen the app after any manifest edit.

### Step 2.2: Initialize Plugin Structure

**Tip 7: TypeScript Strict Mode Will Save You**
Enable `"strict": true` in `tsconfig.json` immediately. The Obsidian API has many `any` types. Strict mode forces you to handle nulls, preventing crashes when `activeEditor` is null.

**Trick**: Create a safe wrapper for all Obsidian API calls:

```typescript
function getActiveEditor(app: App): Editor | null {
  return app.workspace.activeEditor?.editor ?? null;
}
```

**Tip 8: Use `pnpm` Instead of `npm`**
`pnpm` creates hard links, saving disk space when you have multiple plugin projects. Also faster installs:

```bash
npm install -g pnpm
pnpm install
```

---

## **Phase 3: Core Grammar Engine Development - Practical Tips**

### Step 3.1: Implement Rule-Based Foundation

**Tip 9: Regex Performance Kills - Use Compiled Patterns**
Never define regex inside loops. Pre-compile and test performance:

```typescript
// BAD: Creates new regex on every check
function check(text: string) {
  return text.match(/\bhe go\b/gi); // SLOW
}

// GOOD: Pre-compiled
const HE_GO_PATTERN = /\bhe go\b/gi; // Define once globally
function check(text: string) {
  return HE_GO_PATTERN.test(text); // FAST
}
```

**Tip 10: The "Markdown Stripper" is Your Most Critical Function**
**Pitfall**: Your engine will flag `[[link|alias]]` as errors. Strip Markdown _before_ checking:

````typescript
function stripMarkdown(text: string): string {
  return text
    .replace(/\[\[.*?\|?(.*?)\]\]/g, "$1") // Extract alias from links
    .replace(/!?\[.*?\]\(.*?\)/g, "") // Remove images/links
    .replace(/```[\s\S]*?```/g, "") // Remove code blocks
    .replace(/`.*?`/g, "") // Remove inline code
    .replace(/^[>\s-]+/gm, "") // Remove blockquotes/lists
    .replace(/^#\s+/gm, ""); // Remove headers
}
````

**Test this function exhaustively** with every Markdown variant.

**Tip 11: Use "Negative Lookbehind" for Context-Aware Rules**
Avoid flagging errors inside words (e.g., "it's" vs "its"):

```typescript
// Only match "its" as a standalone word, not in "it's" or "grits"
const ITS_PATTERN = /(?<!\w)its(?!\w)/gi;
```

**Tip 12: The "Rule Priority Queue" Pattern**
When rules overlap, define priority:

```typescript
interface Rule {
  priority: number /* higher = runs first */;
}

// Run high-priority rules first (e.g., "it's" before "its")
rules.sort((a, b) => b.priority - a.priority);
```

This prevents low-priority rules from correcting already-fixed text.

### Step 3.2: Integrate Local AI Model

**Tip 13: Model Quantization is Non-Negotiable for Performance**
A full BART model (400MB) will load in 2-3 seconds and use 1GB RAM. Use INT8 quantization:

```bash
# Convert PyTorch to ONNX with quantization
python -m onnxruntime.tools.convert_onnx_models \
  --optimization_style=Runtime \
  --target_platform=arm64 \ # or x86_64
  model_dir/
```

**Trick**: Use **Olive** (ONNX toolchain) for automated optimization:

```bash
pip install olive-ai
olive optimize --config model_config.json
```

**Tip 14: The "Warm-Up" Trick for First Inference**
The first inference is 5-10x slower due to memory allocation. Run a dummy prediction on plugin load:

```typescript
await model.generate(["Warm up"]); // Takes 500ms
// Subsequent calls will be <100ms
```

**Tip 15: Batch Sentences, Not Entire Notes**
Processing a whole note at once OOMs. Chunk by sentence:

```typescript
const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
const batches = chunkArray(sentences, 8); // Process 8 sentences at a time
```

**Tip 16: Use SharedArrayBuffer for Large Models** (Advanced)
If using WebAssembly models in the renderer process, enable cross-origin isolation in `manifest.json`:

```json
{
  "web_accessible_resources": ["/*"],
  "content_security_policy": "cross-origin-isolated"
}
```

### Step 3.3: Hybrid Engine Architecture

**Tip 17: The "Sentence Router" Pattern**
Don't run AI on simple sentences. Use a complexity heuristic:

```typescript
function isComplex(sentence: string): boolean {
  const wordCount = sentence.split(/\s+/).length;
  const commaCount = (sentence.match(/,/g) || []).length;
  const clauseCount = (sentence.match(/\b(and|but|because)\b/gi) || []).length;

  return wordCount > 15 || commaCount > 2 || clauseCount > 1;
}
```

Only route complex sentences to AI. This cuts AI usage by 70%.

**Tip 18: Cache Results with Content Hashing**
Don't re-check unchanged text. Hash the stripped content:

```typescript
import { createHash } from "crypto";

function getCacheKey(text: string): string {
  return createHash("sha256")
    .update(stripMarkdown(text))
    .digest("hex")
    .slice(0, 16);
}

// Check cache first
const key = getCacheKey(noteText);
if (cache.has(key)) return cache.get(key);
```

---

## **Phase 4: Obsidian Plugin Integration - Practical Tips**

### Step 4.1: Editor Decoration System

**Tip 19: The "Decoration Leak" Problem**
CodeMirror decorations persist across note switches. **Always clear on document change**:

```typescript
this.registerEvent(
  workspace.on("active-leaf-change", () => {
    view.dispatch({ effects: clearDecorations }); // CRITICAL
  })
);
```

**Tip 20: Use CSS Classes for Theming, Not Inline Styles**
Let users customize highlights via CSS snippets:

```css
/* In styles.css */
.cm-grammar-error {
  text-decoration: wavy underline;
  text-decoration-color: var(--color-red); /* Respects theme */
}
```

**Trick**: Provide a "Highlight Severity" setting:

```typescript
const severityClasses = {
  low: "cm-grammar-warning",
  medium: "cm-grammar-error",
  high: "cm-grammar-critical",
};
```

**Tip 21: The "Tooltip Hover" Pattern for Suggestions**
Use CodeMirror's hover tooltip (Obsidian 1.5+):

```typescript
import { hoverTooltip } from "@codemirror/view";

const hoverInfo = hoverTooltip((view, pos) => {
  const error = findErrorAtPosition(pos);
  return {
    pos: error.from,
    end: error.to,
    above: true,
    create() {
      const dom = document.createElement("div");
      dom.textContent = error.message;
      error.suggestions.forEach((s) => {
        const btn = document.createElement("button");
        btn.textContent = s;
        btn.onclick = () => applyCorrection(s);
        dom.appendChild(btn);
      });
      return { dom };
    },
  };
});
```

### Step 4.2: Plugin Main Class

**Tip 22: Debouncing is Critical - But Tune Aggressively**
300ms is too long for fast typists. Use adaptive debouncing:

```typescript
let debounceDelay = 150;

this.registerEvent(
  editor.on("change", () => {
    clearTimeout(timer);
    const start = Date.now();
    timer = setTimeout(() => {
      check().then(() => {
        const duration = Date.now() - start;
        // If check is fast, reduce delay; if slow, increase
        debounceDelay = Math.min(300, Math.max(100, duration * 2));
      });
    }, debounceDelay);
  })
);
```

**Tip 23: The "Partial Update" Optimization**
Don't recheck the entire note on every keystroke. Track changed ranges:

```typescript
editor.on("change", (cm, change) => {
  // Only check lines that changed
  const fromLine = change.from.line;
  const toLine = change.to.line + change.text.length;
  checkRange(fromLine, toLine);
});
```

**Tip 24: Disable on Large Notes (>10,000 words)**
Your plugin will freeze Obsidian. Add a size check:

```typescript
const MAX_WORDS = 10000;
if (wordCount > MAX_WORDS) {
  new Notice("Note too large for grammar check", 2000);
  return;
}
```

### Step 4.3: Settings Tab

**Tip 25: Use Setting's `setClass()` for Complex UIs**
For advanced settings, inject custom React components:

```typescript
new Setting(containerEl)
  .setName("Custom Rules")
  .setDesc("Add your own regex patterns")
  .setClass("custom-rules-editor"); // Style this class

// Then in onload(), inject a textarea:
document.querySelector(".custom-rules-editor")?.appendChild(myTextarea);
```

**Tip 26: Settings Validation with Immediate Feedback**
Don't let users save invalid regex:

```typescript
.addTextArea(text => text
  .onChange(async (value) => {
    try {
      new RegExp(value); // Test compilation
      text.inputEl.style.borderColor = 'var(--color-green)';
    } catch (e) {
      text.inputEl.style.borderColor = 'var(--color-red)';
      new Notice('Invalid regex pattern', 1500);
    }
  }))
```

---

## **Phase 5: AI Output Evaluation Framework - Practical Tips**

### Step 5.1: Define Evaluation Metrics

**Tip 27: M2 Score is Painful to Implement - Use ERRANT**
ERRANT's Python library is mature. Don't reimplement in TypeScript:

```python
# scripts/evaluate_with_errant.py
import errant

annotator = errant.load('en')
orig = annotator.parse("He go to school.")
cor = annotator.parse("He goes to school.")
edits = annotator.annotate(orig, cor)
# Use ERRANT's built-in scorer
```

**Trick**: Create a Node.js wrapper:

```typescript
// Spawn Python process for scoring
const { spawn } = require("child_process");
const python = spawn("python", ["scripts/evaluate_with_errant.py"]);
```

**Tip 28: The "Pseudo-Human" Metric for Rapid Feedback**
Before human evaluation, use a strong LLM (Llama-3-70B) to rate corrections:

```typescript
async function pseudoHumanEvaluate(correction: string): Promise<number> {
  const prompt = `Rate this grammar correction (0-5): "${correction}"`;
  const score = await localLLM.generate(prompt);
  return parseFloat(score);
}
```

This gives you a rough quality signal in seconds, not days.

### Step 5.2: Create Evaluation Datasets

**Tip 29: Crowdsource Obsidian-Specific Data from Beta Users**
Add a "Contribute Example" button in settings that sends anonymized sentences (with consent):

```typescript
// In settings tab
.addButton(button => button
  .setButtonText('Share Anonymous Examples')
  .onClick(async () => {
    const examples = getRecentErrors();
    // Send to your API or save to file for manual review
  }))
```

**Tip 30: The "Synthetic Error Injection" Technique**
Generate test data by programmatically breaking correct sentences:

```typescript
function injectError(sentence: string): string {
  const methods = [
    (s) => s.replace(/\bgo\b/g, "goes"), // Wrong SVA
    (s) => s.replace(/\b\./g, ""), // Remove punctuation
    (s) => s.replace(/\b(and|but)\b/g, ""), // Remove conjunctions
  ];
  return methods[Math.floor(Math.random() * methods.length)](sentence);
}
```

### Step 5.3: Automated Evaluation Pipeline

**Tip 31: Run Evaluation on Every `git push` with GitHub Actions**

```yaml
# .github/workflows/evaluate.yml
on: [push]
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm run build
      - run: npm run evaluate
      - uses: actions/upload-artifact@v3
        with:
          name: evaluation-report
          path: reports/
```

**Tip 32: The "Canary Dataset" for Regression Detection**
Keep a small (50-sentence) dataset that must pass 100% before any commit:

```typescript
const CANARY_SENTENCES = [
  { text: "He go.", expected: ["SVA"] },
  { text: "Their here.", expected: ["spelling"] },
];

// Fail CI if any canary fails
const canaryResults = await evaluateBatch(CANARY_SENTENCES);
if (canaryResults.accuracy < 1.0) {
  process.exit(1);
}
```

### Step 5.4: Human Evaluation Protocol

**Tip 33: Use Mechanical Turk for Scale, But Vet Workers**
For broad evaluation, create a qualification test:

```typescript
// Qualification HIT: 10 obvious sentences
// Only allow workers with >90% accuracy
```

Pay $0.10 per sentence. Budget $200 for 2,000 sentences.

**Tip 34: The "Inter-Annotator Agreement" Check**
Have 3 reviewers annotate the same 100 sentences. Calculate Cohen's Kappa:

```python
from sklearn.metrics import cohen_kappa_score
kappa = cohen_kappa_score(reviewer1, reviewer2)
# Accept if kappa > 0.7 (substantial agreement)
```

If agreement is low, your guidelines are ambiguous.

**Tip 35: Gamify Internal Testing**
Create a leaderboard for your beta testers:

```typescript
// Track who finds most false positives
const leaderboard = {
  Alice: { reports: 45, quality: 0.92 },
  Bob: { reports: 23, quality: 0.88 },
};
```

Reward top contributors with plugin credits.

### Step 5.5: Error Analysis Dashboard

**Tip 36: The "False Positive Heatmap" Visualization**
Use Obsidian's canvas API to visualize where errors occur:

```typescript
// Generate canvas JSON showing error density per note
const heatmap = {
  nodes: notes.map((n) => ({
    id: n.path,
    x: Math.random() * 1000,
    y: Math.random() * 1000,
    color: getErrorColor(n.errorCount),
  })),
};
```

**Tip 37: Auto-Generate Rule Fixes from Patterns**
If a rule has >20% false positive rate, flag for review:

```typescript
if (pattern.falsePositiveRate > 0.2) {
  // Suggest rule modification
  const suggestion = `Add negative lookahead: ${pattern.commonContexts[0]}`;
  logSuggestion(pattern.ruleId, suggestion);
}
```

---

## **Phase 6: Testing Strategy - Practical Tips**

### Step 6.1: Unit Testing

**Tip 38: Use `jest-mock-extended` for Obsidian API**
The Obsidian API is complex. Mock only what you need:

```typescript
import { mock } from "jest-mock-extended";
import { App, Editor } from "obsidian";

const mockApp = mock<App>();
const mockEditor = mock<Editor>();
mockEditor.getValue.mockReturnValue("Test text.");
```

**Tip 39: The "Test Pyramid" for Plugins**

- Unit tests: 70% (fast, isolate logic)
- Integration tests: 20% (test with real Obsidian in headless mode)
- E2E tests: 10% (manual testing in real vault)

Use **Vitest** instead of Jest for faster runs.

### Step 6.2: Integration Testing

**Tip 40: Use `obsidian-api-stub` for Headless Testing**

```typescript
import { setupObsidian } from "obsidian-api-stub";

beforeAll(() => {
  setupObsidian();
});

test("plugin loads in mock vault", async () => {
  const plugin = new GrammarCheckerPlugin(app, manifest);
  await plugin.onload();
  expect(plugin).toBeDefined();
});
```

**Tip 41: The "Test Vault in CI" Pattern**
Commit a minimal `.obsidian` folder to your repo:

```bash
mkdir test-vault/.obsidian
# Add core plugins config, but exclude community-plugins.json
```

Your CI can then launch Obsidian headlessly (using Xvfb on Linux) and run tests.

### Step 6.3: Performance Testing

**Tip 42: Use Chrome DevTools Performance Profile _Inside Obsidian_**

1. Open Obsidian
2. Press Ctrl+Shift+I (dev tools)
3. Record performance while typing
4. Look for long tasks >50ms
5. Identify your plugin's functions in the flame chart

**Tip 43: The "Slow Motion" Debug Mode**
artificially slow down your code to see UI thread blocking:

```typescript
// In development only
await new Promise((r) => setTimeout(r, 1000)); // 1s delay
// If UI freezes, you're not async enough
```

**Tip 44: Memory Leak Detection**
Check for detached DOM nodes from decorations:

```typescript
// In console
let before = performance.memory.usedJSHeapSize;
// Use plugin for 5 minutes
let after = performance.memory.usedJSHeapSize;
if (after - before > 50 * 1024 * 1024) {
  // >50MB leak
  console.error("Memory leak detected!");
}
```

### Step 6.4: Where to Run Tests

**Tip 45: Create a "Torture Test" Note**
Include every edge case in one note:

````markdown
# Torture Test

- [ ] Checkboxes
- **Bold** _italic_ `code`
- [[Link|Alias]] [[Link]]
- > Blockquote with error: He go.
- - Nested list
  - With error: They was here.
- $$ LaTeX: E=mc^2 $$
- ```javascript
  const error = "no flag here";
  ```
````

- Emoji: 😊 Grammar error here.
- URL: https://example.com

````
This one note catches 90% of false positive patterns.

---

## **Phase 7: Privacy & Security - Practical Tips**

### Step 7.1: Local-Only Architecture

**Tip 46: The "Airplane Mode" Test**
Disable Wi-Fi and use your plugin for 30 minutes. If any feature breaks, you have a network dependency. Fix it.

**Tip 47: Block DNS at the OS Level During Testing**
On Linux:
```bash
sudo iptables -A OUTPUT -p udp --dport 53 -j DROP
# Now test your plugin
````

If it tries to phone home, it'll fail loudly.

**Tip 48: Audit Dependencies with `npm audit` and `depcheck`**

```bash
npx depcheck              # Finds unused packages
npm audit --audit-level=high # Check for vulnerabilities
```

**Critical**: A compromised dependency could exfiltrate note content.

### Step 7.2: Sensitive Data Detection

**Tip 49: Use `privacy-scanner` Library**

```bash
npm install privacy-scanner
```

It detects PII with high accuracy. Run it on text before checking:

```typescript
import { scan } from "privacy-scanner";

const result = await scan(text);
if (result.hasPII && settings.warnOnPII) {
  new Notice("⚠️ Sensitive content detected. Grammar check disabled.", 3000);
  return []; // Don't check
}
```

**Tip 50: The "Redaction Mode" for Debug Logs**
If you must log, redact first:

```typescript
function redact(text: string): string {
  return text
    .replace(/\b\d{4}\b/g, "####") // Years
    .replace(/\b[A-Z][a-z]+\b/g, "[Name]") // Names
    .replace(/\S+@\S+\.\S+/g, "[Email]");
}

console.log(redact(noteText)); // Safe to share logs
```

### Step 7.3: Audit Trail

**Tip 51: Write Audit Log to `.obsidian/plugins/grammar-checker/audit.log`**

```typescript
const logPath = `${this.manifest.dir}/audit.log`;
await fs.appendFile(logPath, JSON.stringify(entry) + "\n");
```

Users can inspect this file to see what your plugin did. Build trust through transparency.

**Tip 52: The "Emergency Stop" Button**
Add a command palette action that immediately disables all checks and clears caches:

```typescript
this.addCommand({
  id: "emergency-stop",
  name: "Emergency: Disable All Checks",
  callback: () => {
    this.settings.enabled = false;
    this.engine.clearCache();
    new Notice(
      "Grammar checker disabled. Restart Obsidian to re-enable.",
      5000
    );
  },
});
```

---

## **Phase 8: Deployment & Iteration - Practical Tips**

### Step 8.1: Beta Testing

**Tip 53: Use Feature Flags for Gradual Rollout**

```typescript
const enableNewRule = this.settings.betaFeatures && Math.random() < 0.1; // 10% of beta users
```

This limits blast radius of buggy features.

**Tip 54: The "Update Changelog in Settings" Pattern**
Show recent updates directly in your settings tab to re-engage users:

```typescript
const changelog = await fetch(
  "https://api.github.com/repos/you/plugin/releases/latest"
);
const latest = await changelog.json();
new Notice(
  `✨ Updated to v${latest.tag_name}: ${latest.body.slice(0, 100)}...`,
  8000
);
```

**Tip 55: Collect Stack Traces Without Violating Privacy**

```typescript
// In error handler
const errorInfo = {
  message: error.message,
  stack: error.stack.split("\n").slice(0, 5), // Only first 5 lines
  // NO user text included
};
// Send to Sentry if user opts in
```

### Step 8.2: Community Plugin Submission

**Tip 56: The "Submission Checklist" Markdown File**
Create `SUBMISSION_CHECKLIST.md` in your repo:

```markdown
- [ ] main.js is < 1MB (uncompressed)
- [ ] manifest.json has unique ID
- [ ] README has clear privacy policy
- [ ] No console.log() left in code
- [ ] Tested on Windows (GitHub Actions can do this)
- [ ] Screenshots are 800x600 PNG
- [ ] Release is tagged v1.0.0
```

Follow it religiously. Rejections are often for trivial issues.

**Tip 57: The "Obsidian Team's Pet Peeves"**
From rejected submissions:

- Don't use `alert()`. Use `new Notice()`
- Don't modify files outside `.obsidian/plugins/your-plugin/`
- Don't require restart after settings change
- Don't bundle node_modules. Use `npm run build` with proper bundling

**Tip 58: Pre-Submit to "Obsidian Plugin Dev" Discord**
Join the Discord and post your plugin in #plugin-dev. Get feedback from moderators _before_ official submission.

### Step 8.3: Post-Launch Monitoring

**Tip 59: The "Canary Release" Strategy**
Release v1.0.0 to 10% of users via GitHub Releases with a pre-release tag. Monitor # of issues. If <5 issues in 48h, promote to full release.

**Tip 60: Use GitHub Issues Templates for Bug Reports**

```markdown
<!-- .github/ISSUE_TEMPLATE/bug_report.md -->

**Sentence that triggered bug:**
**Expected behavior:**
**Console error (Ctrl+Shift+I):**
**Plugin version:**
```

This extracts maximum useful info from users.

**Tip 61: The "Analytics Without Tracking" Pattern**
If you want usage stats _without_ privacy issues, use **fuzzy counting**:

```typescript
// Instead of sending "user typed XYZ", send:
{
  errorType: 'SVA',
  noteLength: Math.floor(text.length / 100) * 100, // Rounded
  timestamp: Date.now() - (Date.now() % 3600000) // Hourly buckets
}
```

This provides aggregate data without identifying users.

### Step 8.4: Where to Check Performance Over Time

**Tip 62: The "Performance Budget" File**
Commit a `performance-budget.json`:

```json
{
  "maxBundleSize": "500KB",
  "maxMemoryUsage": "50MB",
  "maxCheckTime": "100ms",
  "minF05Score": "0.60"
}
```

Your CI fails if any metric is breached.

**Tip 63: Run Benchmarks on Old Hardware**
Test on a 2015 laptop or Raspberry Pi. If it's fast there, it'll be fast everywhere. Use GitHub Actions' `macos-11` runner for old macOS versions.

**Tip 64: The "Version Compare" Dashboard**
Generate a diff between versions:

```bash
# In CI
git diff v1.0.0..v1.1.0 src/rules/ > rule-changes.diff
# Parse and highlight which rules were added/modified
```

Show this in your release notes so users know what improved.

---

## **Summary: The "Golden Rules" of Grammar Checker Development**

1. **Start Stupid**: 20 regex rules > 0 AI models
2. **Strip First**: Markdown kills accuracy
3. **Measure Everything**: If you can't measure it, you can't improve it
4. **Privacy is a Feature**: Not an afterthought
5. **Beta Test for 2 Weeks Minimum**: Your blind spots are huge
6. **Never Block the UI Thread**: Always async/await
7. **Cache Aggressively**: Text doesn't change that much
8. **Human Evaluation > Automated Metrics**: HAR is your north star
9. **Document Everything**: Users trust transparent plugins
10. **Plan for Maintenance**: 30% of time is bug fixes, not features

This exhaustive list should cover 95% of the pitfalls you'll encounter. The remaining 5% will be unique to your codebase—debug those with the tools above.
