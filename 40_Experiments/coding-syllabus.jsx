import { useState } from "react";

const syllabusData = [
  {
    phase: "Foundation",
    phaseNum: 1,
    weeks: "Weeks 1–4",
    color: "#6366f1",
    description: "Build comfort with code concepts and the AI learning workflow.",
    modules: [
      {
        title: "Week 1 — Hello, Programming!",
        goal: "Understand what code is, set up your environment, and write your first program.",
        topics: [
          "What is programming? (real-world analogies)",
          "Choosing a language: Python (recommended for beginners)",
          "Setting up: browser-based IDE (Replit / Google Colab)",
          "Your first program: print(), strings, and comments",
          "How to talk to an AI chatbot for learning (prompting 101)",
        ],
        aiActivities: [
          "Ask the AI: \"Explain variables like I'm ordering coffee\"",
          "Prompt: \"Write a simple program and explain each line\"",
          "Challenge: Have the AI quiz you on what each line does",
        ],
        project: "\"About Me\" script — prints your name, age, hobby, and a fun fact using variables.",
      },
      {
        title: "Week 2 — Data Types & Operations",
        goal: "Work with numbers, text, and basic math in code.",
        topics: [
          "Integers, floats, strings, booleans",
          "Arithmetic operators (+, -, *, /, //, %, **)",
          "String concatenation and f-strings",
          "Type conversion (int(), str(), float())",
          "Input from users: input()",
        ],
        aiActivities: [
          "Ask the AI to generate 5 type-conversion puzzles for you",
          "Prompt: \"What's wrong with this code?\" (paste broken snippets)",
          "Prompt: \"Give me a real-world problem I can solve with math operators\"",
        ],
        project: "Tip Calculator — takes bill amount and tip %, outputs total per person.",
      },
      {
        title: "Week 3 — Decisions & Logic",
        goal: "Make programs that respond differently based on conditions.",
        topics: [
          "Comparison operators (==, !=, <, >, <=, >=)",
          "if / elif / else statements",
          "Logical operators (and, or, not)",
          "Nested conditions",
          "Truthy and falsy values",
        ],
        aiActivities: [
          "Ask: \"Create a flowchart in text for a login system\"",
          "Prompt: \"Give me 3 buggy if-statements to fix\"",
          "Role-play: AI pretends to be the computer — you trace through code together",
        ],
        project: "Grade Calculator — takes a score, outputs letter grade with pass/fail message.",
      },
      {
        title: "Week 4 — Loops & Repetition",
        goal: "Automate repetitive tasks with loops.",
        topics: [
          "for loops and range()",
          "while loops and loop control",
          "break, continue, and loop patterns",
          "Nested loops (intro)",
          "Common patterns: counting, accumulating, searching",
        ],
        aiActivities: [
          "Prompt: \"Explain for vs while loops using a restaurant analogy\"",
          "Ask: \"Generate a loop tracing exercise — show me what prints\"",
          "Challenge: \"Give me a problem, let me try, then review my code\"",
        ],
        project: "Number Guessing Game — computer picks a number, user guesses with hints (higher/lower).",
      },
    ],
  },
  {
    phase: "Building Blocks",
    phaseNum: 2,
    weeks: "Weeks 5–8",
    color: "#8b5cf6",
    description: "Organize code into reusable pieces and work with collections of data.",
    modules: [
      {
        title: "Week 5 — Lists & Collections",
        goal: "Store and manipulate groups of data.",
        topics: [
          "Lists: creating, indexing, slicing",
          "List methods: append, remove, sort, reverse",
          "Iterating through lists",
          "List comprehensions (intro)",
          "Tuples and when to use them",
        ],
        aiActivities: [
          "Prompt: \"Give me a dataset as a list and 5 tasks to perform on it\"",
          "Ask: \"What's the difference between these two approaches?\" (compare solutions)",
          "Challenge: AI gives you output, you write code to produce it",
        ],
        project: "To-Do List Manager — add, remove, view, and mark tasks complete (command-line).",
      },
      {
        title: "Week 6 — Dictionaries & Data Structures",
        goal: "Use key-value pairs to model real-world data.",
        topics: [
          "Dictionaries: creating, accessing, updating",
          "Dictionary methods: keys(), values(), items()",
          "Nested dictionaries",
          "Sets (intro)",
          "Choosing the right data structure",
        ],
        aiActivities: [
          "Prompt: \"Model a restaurant menu as a dictionary and give me tasks\"",
          "Ask: \"When should I use a list vs dict vs set? Give examples\"",
          "Pair-program with AI: build a phone book app together step by step",
        ],
        project: "Contact Book — store names, phones, emails; search, add, delete contacts.",
      },
      {
        title: "Week 7 — Functions",
        goal: "Write reusable, organized code blocks.",
        topics: [
          "Defining and calling functions",
          "Parameters, arguments, return values",
          "Default and keyword arguments",
          "Scope: local vs global variables",
          "Docstrings and clean code practices",
        ],
        aiActivities: [
          "Prompt: \"Here's my messy code — help me refactor it into functions\"",
          "Ask: \"Explain scope using a house/rooms metaphor\"",
          "Challenge: AI describes a task, you write the function signature first, then implement",
        ],
        project: "Password Generator — function that creates passwords with customizable length, complexity.",
      },
      {
        title: "Week 8 — File Handling & Error Management",
        goal: "Read/write files and handle things that go wrong gracefully.",
        topics: [
          "Reading and writing text files",
          "CSV files basics",
          "try / except / finally",
          "Common exceptions and how to handle them",
          "Intro to debugging strategies",
        ],
        aiActivities: [
          "Prompt: \"Give me code with 5 hidden bugs — I'll find and fix them\"",
          "Ask: \"What errors would this code cause and why?\"",
          "Strategy session: \"How should I approach debugging this error message?\"",
        ],
        project: "Expense Tracker — log expenses to a CSV, read totals by category, handle bad input.",
      },
    ],
  },
  {
    phase: "Real-World Skills",
    phaseNum: 3,
    weeks: "Weeks 9–12",
    color: "#a855f7",
    description: "Apply your skills to practical projects using external tools and APIs.",
    modules: [
      {
        title: "Week 9 — Modules, Libraries & APIs",
        goal: "Leverage other people's code and connect to the internet.",
        topics: [
          "Importing modules (random, math, datetime, os)",
          "Installing packages with pip",
          "Working with JSON data",
          "API basics: requests library, GET requests",
          "Reading API documentation",
        ],
        aiActivities: [
          "Prompt: \"Walk me through calling a weather API step by step\"",
          "Ask: \"Explain JSON like I'm organizing a filing cabinet\"",
          "Challenge: AI picks a public API, you build a script to fetch and display data",
        ],
        project: "Weather Dashboard — fetch weather data from an API and display a formatted report.",
      },
      {
        title: "Week 10 — Object-Oriented Programming",
        goal: "Model real-world things as objects in code.",
        topics: [
          "Classes and objects: the blueprint metaphor",
          "Attributes and methods",
          "__init__ and self",
          "Inheritance basics",
          "When to use OOP vs functions",
        ],
        aiActivities: [
          "Prompt: \"Help me design a class for a Library system — ask me questions first\"",
          "Ask: \"Review my class design — what am I missing?\"",
          "Role-play: AI is the 'object', you call methods on it and it responds",
        ],
        project: "Bank Account System — classes for Account, SavingsAccount; deposit, withdraw, transfer.",
      },
      {
        title: "Week 11 — Web Basics & Automation",
        goal: "Build a simple web page or automate a boring task.",
        topics: [
          "HTML & CSS crash course",
          "Flask: your first web app (2 routes)",
          "OR: Automation with Python (web scraping basics, file automation)",
          "Virtual environments",
          "Deploying a simple project",
        ],
        aiActivities: [
          "Prompt: \"Help me build a personal portfolio page, one section at a time\"",
          "Ask: \"I do [X task] weekly — can you help me automate it?\"",
          "Pair-program: build a Flask app with AI guiding architecture decisions",
        ],
        project: "Choose your path: Mini Web App (Flask) OR Task Automator (automate a real personal task).",
      },
      {
        title: "Week 12 — Capstone & Learning Roadmap",
        goal: "Consolidate everything into a portfolio-worthy project.",
        topics: [
          "Project planning & breaking problems into steps",
          "Code review practices",
          "Git & GitHub basics (version control)",
          "Building a learning roadmap for continued growth",
          "How to use AI effectively as a ongoing coding partner",
        ],
        aiActivities: [
          "Prompt: \"I want to build [X]. Help me break this into milestones\"",
          "Code review: \"Here's my capstone code. Review it like a senior developer\"",
          "Planning: \"Based on what I've learned, suggest my next 3-month learning path\"",
        ],
        project: "Capstone Project — student's choice. Examples: Quiz App, Budget Planner, Recipe Finder, Personal Dashboard.",
      },
    ],
  },
];

const aiPromptingGuide = [
  { emoji: "🟢", label: "Learn", example: "\"Explain [concept] like I'm 10 years old\"" },
  { emoji: "🔵", label: "Practice", example: "\"Give me 5 exercises on [topic], easy → hard\"" },
  { emoji: "🟡", label: "Debug", example: "\"Here's my code and the error. Don't fix it — guide me to the answer\"" },
  { emoji: "🟠", label: "Review", example: "\"Review my code. What would a senior developer change?\"" },
  { emoji: "🔴", label: "Challenge", example: "\"Give me a problem I'm not ready for, then help me through it\"" },
];

function ChevronDown({ open }) {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style={{ transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
      <path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M3 8L6.5 11.5L13 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function ModuleCard({ module, index, completed, onToggle }) {
  const [open, setOpen] = useState(false);

  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 12, marginBottom: 12, overflow: "hidden", background: completed ? "#f0fdf4" : "#fff", transition: "background 0.3s" }}>
      <button
        onClick={() => setOpen(!open)}
        style={{ width: "100%", padding: "16px 20px", display: "flex", alignItems: "center", gap: 12, border: "none", background: "none", cursor: "pointer", textAlign: "left", fontSize: 15 }}
      >
        <button
          onClick={(e) => { e.stopPropagation(); onToggle(); }}
          style={{
            width: 26, height: 26, borderRadius: 8, border: completed ? "2px solid #22c55e" : "2px solid #cbd5e1",
            background: completed ? "#22c55e" : "transparent", display: "flex", alignItems: "center", justifyContent: "center",
            cursor: "pointer", color: "#fff", flexShrink: 0, transition: "all 0.2s",
          }}
        >
          {completed && <CheckIcon />}
        </button>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, color: "#1e293b", textDecoration: completed ? "line-through" : "none", opacity: completed ? 0.6 : 1 }}>{module.title}</div>
          <div style={{ fontSize: 13, color: "#64748b", marginTop: 2 }}>{module.goal}</div>
        </div>
        <ChevronDown open={open} />
      </button>

      {open && (
        <div style={{ padding: "0 20px 20px", borderTop: "1px solid #f1f5f9" }}>
          <div style={{ display: "grid", gap: 16, marginTop: 16 }}>
            <Section title="📚 Topics" items={module.topics} />
            <Section title="🤖 AI Chatbot Activities" items={module.aiActivities} highlight />
            <div style={{ background: "#fefce8", borderRadius: 10, padding: 14 }}>
              <div style={{ fontWeight: 600, fontSize: 13, color: "#a16207", marginBottom: 4 }}>🛠️ Mini Project</div>
              <div style={{ fontSize: 14, color: "#854d0e" }}>{module.project}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Section({ title, items, highlight }) {
  return (
    <div style={{ background: highlight ? "#eff6ff" : "#f8fafc", borderRadius: 10, padding: 14 }}>
      <div style={{ fontWeight: 600, fontSize: 13, color: highlight ? "#1d4ed8" : "#475569", marginBottom: 8 }}>{title}</div>
      <ul style={{ margin: 0, paddingLeft: 18, display: "flex", flexDirection: "column", gap: 4 }}>
        {items.map((item, i) => (
          <li key={i} style={{ fontSize: 14, color: highlight ? "#1e40af" : "#334155", lineHeight: 1.5 }}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default function CodingSyllabus() {
  const [completed, setCompleted] = useState({});
  const [activePhase, setActivePhase] = useState(0);
  const [showGuide, setShowGuide] = useState(false);

  const totalModules = syllabusData.reduce((sum, p) => sum + p.modules.length, 0);
  const completedCount = Object.values(completed).filter(Boolean).length;
  const progress = Math.round((completedCount / totalModules) * 100);

  const toggleModule = (key) => {
    setCompleted((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: "24px 16px", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 32 }}>
        <div style={{ fontSize: 40, marginBottom: 8 }}>💻</div>
        <h1 style={{ fontSize: 26, fontWeight: 700, color: "#0f172a", margin: "0 0 6px" }}>Learn to Code with AI</h1>
        <p style={{ fontSize: 15, color: "#64748b", margin: 0 }}>A 12-week structured syllabus for adult beginners</p>
        <p style={{ fontSize: 13, color: "#94a3b8", margin: "4px 0 0" }}>Python · AI-Assisted · Project-Based</p>
      </div>

      {/* Progress */}
      <div style={{ background: "#f8fafc", borderRadius: 12, padding: 16, marginBottom: 24, border: "1px solid #e2e8f0" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
          <span style={{ fontSize: 14, fontWeight: 600, color: "#334155" }}>Progress</span>
          <span style={{ fontSize: 14, color: "#64748b" }}>{completedCount}/{totalModules} weeks · {progress}%</span>
        </div>
        <div style={{ height: 10, background: "#e2e8f0", borderRadius: 99, overflow: "hidden" }}>
          <div style={{ height: "100%", width: `${progress}%`, background: "linear-gradient(90deg, #6366f1, #a855f7)", borderRadius: 99, transition: "width 0.4s ease" }} />
        </div>
      </div>

      {/* AI Prompting Guide Toggle */}
      <button
        onClick={() => setShowGuide(!showGuide)}
        style={{
          width: "100%", padding: "14px 20px", borderRadius: 12, border: "1px solid #c7d2fe", background: "#eef2ff",
          cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24,
          fontSize: 14, fontWeight: 600, color: "#4338ca",
        }}
      >
        <span>🧠 How to Learn with an AI Chatbot — Prompting Guide</span>
        <ChevronDown open={showGuide} />
      </button>
      {showGuide && (
        <div style={{ background: "#eef2ff", borderRadius: 12, padding: 20, marginBottom: 24, marginTop: -16, border: "1px solid #c7d2fe" }}>
          <p style={{ fontSize: 14, color: "#3730a3", margin: "0 0 16px", lineHeight: 1.6 }}>
            Use these 5 prompting strategies throughout the course. The key is to <strong>never just ask for the answer</strong> — ask the AI to teach, challenge, and review you.
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {aiPromptingGuide.map((item, i) => (
              <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start", background: "#fff", borderRadius: 10, padding: 12 }}>
                <span style={{ fontSize: 20, flexShrink: 0 }}>{item.emoji}</span>
                <div>
                  <div style={{ fontWeight: 600, fontSize: 14, color: "#1e1b4b" }}>{item.label}</div>
                  <div style={{ fontSize: 13, color: "#4338ca", fontStyle: "italic" }}>{item.example}</div>
                </div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 16, padding: 12, background: "#fff", borderRadius: 10, border: "1px dashed #a5b4fc" }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#4338ca", marginBottom: 4 }}>💡 Golden Rule</div>
            <div style={{ fontSize: 13, color: "#3730a3", lineHeight: 1.5 }}>
              Always try first, then ask the AI. Frame requests as: "Here's what I tried → Here's what happened → Help me understand why."
            </div>
          </div>
        </div>
      )}

      {/* Phase Tabs */}
      <div style={{ display: "flex", gap: 8, marginBottom: 20, overflowX: "auto" }}>
        {syllabusData.map((phase, i) => (
          <button
            key={i}
            onClick={() => setActivePhase(i)}
            style={{
              padding: "10px 16px", borderRadius: 10, border: activePhase === i ? `2px solid ${phase.color}` : "2px solid #e2e8f0",
              background: activePhase === i ? `${phase.color}10` : "#fff", cursor: "pointer", whiteSpace: "nowrap",
              fontSize: 13, fontWeight: 600, color: activePhase === i ? phase.color : "#64748b", transition: "all 0.2s",
            }}
          >
            Phase {phase.phaseNum}: {phase.phase}
          </button>
        ))}
      </div>

      {/* Active Phase Content */}
      {syllabusData.map((phase, phaseIdx) => (
        phaseIdx === activePhase && (
          <div key={phaseIdx}>
            <div style={{ marginBottom: 20 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                <div style={{ width: 8, height: 8, borderRadius: 99, background: phase.color }} />
                <h2 style={{ margin: 0, fontSize: 20, fontWeight: 700, color: "#0f172a" }}>
                  Phase {phase.phaseNum}: {phase.phase}
                </h2>
              </div>
              <p style={{ margin: "0 0 0 18px", fontSize: 14, color: "#64748b" }}>{phase.weeks} — {phase.description}</p>
            </div>

            {phase.modules.map((mod, modIdx) => {
              const key = `${phaseIdx}-${modIdx}`;
              return (
                <ModuleCard
                  key={key}
                  module={mod}
                  index={modIdx}
                  completed={!!completed[key]}
                  onToggle={() => toggleModule(key)}
                />
              );
            })}
          </div>
        )
      ))}

      {/* Footer */}
      <div style={{ marginTop: 32, padding: 20, background: "#f8fafc", borderRadius: 12, textAlign: "center", border: "1px solid #e2e8f0" }}>
        <div style={{ fontSize: 18, marginBottom: 6 }}>🎓</div>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#334155", marginBottom: 4 }}>After the 12 Weeks</div>
        <p style={{ fontSize: 13, color: "#64748b", margin: 0, lineHeight: 1.6 }}>
          You'll have 12 projects, a GitHub portfolio, and the skills to keep learning independently with AI as your coding partner. Suggested next steps: data science, web development, or automation.
        </p>
      </div>
    </div>
  );
}
