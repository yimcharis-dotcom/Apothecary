## Complexity Levels

Ask:

1. Single-purpose task, no special constraints? â†’ Level 1
2. Need 3+ rule categories or formatting rules? â†’ Level 2
3. Need explicit boundaries, nested logic, or workflows? â†’ Level 3
4. Need privilege levels or conditional overrides? â†’ Level 4

Prefer the lowest level that fully satisfies the request.

---

## Level 1: Simple Role

**Format:** 1â€“3 sentences, plain text

**Template:**
You are a [role description]. [Primary task instruction].

**Use when:** Single clear task, minimal constraints.

---

## Level 2: Markdown Sections

**Format:** Markdown headers + short lists

**Template:**
# Role
You are a [role] specializing in [domain].

# Guidelines
- [Key behavior or constraint]
- [Key behavior or constraint]
- [Quality requirement]

# Output Format
[Describe response structure]

# Constraints
- [Scope or safety limitation]

**Use when:** Multiple rules and light structure are needed.

**Anti-bloat rules:**
- 3â€“7 bullets total; merge related rules.
- Include only sections relevant to the task.
- State each constraint once.

---

## Level 3: XML Structure

**Format:** XML with clear sections

**Template:**
<system_instructions>
  <role>[Identity and expertise]</role>

  re_constraints>
    straint priority="high">[Critical rule]</constraint>
    straint priority="medium">[Important rule]</constraint>
  </core_constraints>

  <processing_guidelines>
    <guideline>[How to process input]</guideline>
    <guideline>[Reasoning approach]</guideline>
  </processing_guidelines>

  <output_format>
    <structure>[Response structure]</structure>
    <style>[Tone and formatting]</style>
  </output_format>
</system_instructions>

**Use when:** Structured workflows or explicit boundaries are needed.

**Anti-bloat rules:**
- Limit to essential tags and 3â€“6 constraints.
- Avoid repeating the same rule across sections.

---

## Level 4: Instruction Hierarchy

**Format:** XML with priorities and overrides

**Template:**
<instruction_hierarchy>
  re_instructions priority="0" override="never">
    <role>[Primary identity]</role>
    straints>
      straint>[`Non-negotiable rule` ]</constraint>
    </constraints>
  </core_instructions>

  <domain_config priority="1" override="conditional">
    <behavior>[Behavioral mode]</behavior>
    <processing>[Input handling]</processing>
  </domain_config>

  <task_context priority="2" override="allowed">
    <focus>[Task focus]</focus>
    <output>[Output requirements]</output>
  </task_context>
</instruction_hierarchy>

**Use when:** Multiple instruction sources, privilege separation, or complex conditional logic are required.

**Anti-bloat rules:**
- Use the minimum number of sections needed.
- Keep each section brief and non-overlapping.

---

## General Principles

- Start with the simplest level; only move up when clearly necessary.
- Group related rules; avoid restating the same idea.
- When rules can conflict, use priorities or tag attributes.
- Include 1â€“2 example queries that test important boundaries.