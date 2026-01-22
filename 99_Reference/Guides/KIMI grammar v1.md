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
