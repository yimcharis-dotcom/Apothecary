# System Instruction Design Guidelines

## Decision Tree

1. Single-purpose, trusted input? → Level 1
2. Multiple guidelines, no security? → Level 2
3. High-stakes/injection risk? → Level 3
4. Privilege conflicts? → Level 4

## Level 1 Template

You are a \[ROLE]. \[CORE\_TASK].

## Level 2 Template

# Role

You are a \[ROLE] specializing in \[DOMAIN].

# Guidelines

* \[RULE 1]
* \[RULE 2]

# Output Format

\[DESCRIPTION]

## Level 3 Template

<system\_instructions>
<role>\[ROLE]</role>
<core\_constraints>
<constraint>\[CRITICAL RULE]</constraint>
</core\_constraints>
<output\_format>
<structure>\[FORMAT]</structure>
</output\_format>
</system\_instructions>

## Level 4 Template

<instruction\_hierarchy>
<system\_prompt priority="0">
<safety\_constraints>
<constraint>\[SAFETY]</constraint>
</safety\_constraints>
</system\_prompt>
<user\_context priority="2">
<task>\[TASK]</task>
</user\_context>
</instruction\_hierarchy>

## Common Components

**Safety:** Never \[harmful action]. Cite sources.
**Formats:** Markdown lists, tables, code blocks.
**Tones:** Professional, concise.

