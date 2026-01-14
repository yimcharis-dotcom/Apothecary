

1. **Annotated Text**: Show original text with errors marked using [1.], [2.], [3.] citation format. Apply markup:
    - Tier 1: _italics_[\#.]
    - Tier 2: ***bold italics***[\#.]
2. **Explanations** (Tier 2 only):
[\#.] [Prescriptive/Descriptive/Naturalness] "quote" - What's wrong

Rule: [principle]
Impact: [why it matters]
Alternatives: [1–2 rephrasings]
3. **Native Speaker Alternatives**: Provide 2–3 rewrites with register labels (Casual/neutral/Formal (Financial/technical) only when register or phrasing choices significantly differ. For mechanical fixes, one corrected version in section 4 suffices.
4. **Corrected Version**: All errors fixed.
</structure>

<style>Direct and technical. Deep explanations only for subtle issues.</style>
</output_format>
  <constraints>
    ```
    <constraint priority="high">Only mark actual errors—not correct grammar, acceptable collocations, or standard constructions.</constraint>
    ```
    <constraint priority="high">Use [#.] citation format with period for all markers. This format is required for parser compliance.</constraint>
    ```
    <constraint priority="high">Every bold-italics-marked item must have a corresponding explanation in Section 2. If an annotation number appears in Section 1, it must appear in Section 2 unless it's Tier 1 (italics).</constraint>
    ```
    ```
    <constraint priority="high">Provide all four sections. Section 4 must fix every marked error, including those explained in Section 2 and register issues mentioned in explanations.</constraint>
    ```
    <constraint priority="medium">Label each Tier 2 issue as:
    - [Prescriptive]: violates grammar rules or collocations
    - [Descriptive]: register mismatch, tone issue, or pragmatic risk
    - [Naturalness]: grammatically correct but unnatural phrasing/word choice</constraint>
  </constraints>
</system_instructions>

Understood. I've loaded the reference guide and system instructions. I'm ready to evaluate texts as an English grammar and naturalness checker for C1 proficiency users.

Paste any text, and I'll provide:

1. **Annotated Text** (with Tier 1 and Tier 2 markings)
2. **Explanations** (Tier 2 only)
3. **Native Speaker Alternatives**
4. **Corrected Version**

Ready when you are.
<span style="display:none">[^1_1]</span>

<div align="center">⁂</div>

[^1_1]: DvPvN-Grammar-Checker-Tier-Classification-Edge-Cases.md


---

## 1. Annotated Text

***Hey***[1.] Dr. Martinez, I wanted to reach out regarding the quarterly financial statements. The data shows significant revenue ***growth, however***[2.] the board feel the _projections is_[3.] overly optimistic. ***We're doing researches***[4.] on market trends, and based on this analysis, I suggest you reconsider your assumptions ***since your relatively new to this sector***[5.]. The ***equipments***[6.] purchased last quarter was depreciated incorrectly, and _making amendments to the balance sheet are_[7.] critical. Internet connectivity _issues has_[8.] prevented timely reporting. Please _advice_[9.] on how to proceed, as we _need respond_[10.] by _end of week_[11.].

***

## 2. Explanations

**[1.]** [Descriptive] "Hey"

**Rule:** Greeting formality must match document register.
**Impact:** "Hey" signals casual familiarity inappropriate for formal business communication with a senior colleague about quarterly financials and board concerns.
**Alternatives:**

- Dear Dr. Martinez,
- Dr. Martinez,

**[2.]** [Prescriptive] "growth, however"

**Rule:** Conjunctive adverbs joining independent clauses require semicolon + comma or period + capital, not comma alone.
**Impact:** Creates comma splice; "however" cannot join independent clauses with only a comma.
**Alternatives:**

- growth; however, the board
- growth. However, the board

**[4.]** [Prescriptive] "We're doing researches"

**Rule:** "Research" is an uncountable noun; standard collocation is "conducting research" not "doing research."
**Impact:** Double error—incorrect plural form + non-standard verb pairing in formal business context.
**Alternatives:**

- We're conducting research
- We've researched

**[5.]** [Descriptive] "since your relatively new to this sector"

**Rule:** Avoid face-threatening remarks that question a colleague's competence or experience in professional communication.
**Impact:** Undermines Dr. Martinez's authority and creates interpersonal risk; also contains grammar error ("your" → "you're").
**Alternatives:**

- given the evolving nature of this sector
- as market conditions in this sector have shifted recently

**[6.]** [Prescriptive] "equipments"

**Rule:** "Equipment" is an uncountable noun with no plural form.
**Impact:** Non-standard morphology; "equipment" remains singular even when referring to multiple items.
**Alternatives:**

- The equipment
- The pieces of equipment

***

## 3. Native Speaker Alternatives

**Formal (business standard):**

Dr. Martinez, I wanted to reach out regarding the quarterly financial statements. The data shows significant revenue growth; however, the board feels the projections are overly optimistic. We're conducting research on market trends, and based on this analysis, I suggest reconsidering the assumptions given the evolving nature of this sector. The equipment purchased last quarter was depreciated incorrectly, and making amendments to the balance sheet is critical. Internet connectivity issues have prevented timely reporting. Please advise on how to proceed, as we need to respond by the end of the week.

**Alternative (slightly less formal but still professional):**

Dr. Martinez, I'm reaching out about the quarterly financial statements. The data shows strong revenue growth, but the board feels the projections may be overly optimistic. Our research on market trends suggests we should revisit some of the underlying assumptions given recent sector developments. There's also a depreciation error on last quarter's equipment purchases that requires balance sheet amendments. Internet connectivity problems have delayed our reporting. Could you advise on next steps? We need to respond by week's end.

***

## 4. Corrected Version

Dr. Martinez, I wanted to reach out regarding the quarterly financial statements. The data shows significant revenue growth; however, the board feels the projections are overly optimistic. We're conducting research on market trends, and based on this analysis, I suggest you reconsider your assumptions given the evolving nature of this sector. The equipment purchased last quarter was depreciated incorrectly, and making amendments to the balance sheet is critical. Internet connectivity issues have prevented timely reporting. Please advise on how to proceed, as we need to respond by the end of the week.

---

## 1. Annotated Text

So I've been trying to _setup_[1.] the new authentication system for our app, and honestly the documentation ***doesn't really help understanding***[2.] the OAuth flow. ***Me and my team was***[3.] debugging this issue for three days straight. The error _messages keeps_[4.] saying "invalid token" but we're doing everything _correct_[5.] according to the guides. I think the _problem are_[6.] in how the API handles refresh tokens, since _it seem like tokens expires_[7.] too quickly. We _need figure_[8.] out if this behavior is intentional or if there's configuration options we're missing. Has anyone dealt with similar problems? Would appreciate if someone could explain what's the proper way to implement this, because currently our users ***can't barely login***[9.] without getting frustrated.

***

## 2. Explanations

**[2.]** [Naturalness] "doesn't really help understanding"

**Rule:** The verb "help" requires either "help (someone) understand" or "help with understanding"—bare gerund after "help" sounds incomplete.
**Impact:** Grammatically borderline but unnatural to native speakers; the construction feels truncated.
**Alternatives:**

- doesn't really help us understand
- doesn't really help with understanding

**[3.]** [Prescriptive] "Me and my team was"

**Rule:** Subject pronouns precede verbs ("I" not "me"); plural subjects take plural verbs ("were" not "was").
**Impact:** Combines pronoun case error with subject-verb agreement violation; even in informal registers, C1 users should use "My team and I were."
**Alternatives:**

- My team and I were
- My team and I have been

**[9.]** [Prescriptive] "can't barely login"

**Rule:** Double negatives ("can't" + "barely") create logical contradiction; verb form is "log in" (two words), not "login" (noun).
**Impact:** Double negative reverses intended meaning; should be either "can barely" or "can't" but not both.
**Alternatives:**

- can barely log in
- can't log in

***

## 3. Native Speaker Alternatives

**Casual (forum/chat appropriate):**

So I've been trying to set up the new authentication system for our app, and honestly the documentation doesn't really help us understand the OAuth flow. My team and I have been debugging this issue for three days straight. The error messages keep saying "invalid token" but we're doing everything correctly according to the guides. I think the problem is in how the API handles refresh tokens, since it seems like tokens expire too quickly. We need to figure out if this behavior is intentional or if there are configuration options we're missing. Has anyone dealt with similar problems? I'd appreciate if someone could explain the proper way to implement this, because currently our users can barely log in without getting frustrated.

**Alternative (slightly more structured):**

I've been trying to set up the new authentication system, but the documentation hasn't been much help in understanding the OAuth flow. My team and I have spent three days debugging an "invalid token" error, even though we're following the guides correctly. I suspect the problem is in how the API handles refresh tokens—they seem to expire too quickly. We need to figure out whether this is intentional or if we're missing some configuration options. Has anyone experienced this? I'd appreciate any advice on the proper implementation approach, since our users can barely log in right now.

***

## 4. Corrected Version

So I've been trying to set up the new authentication system for our app, and honestly the documentation doesn't really help us understand the OAuth flow. My team and I were debugging this issue for three days straight. The error messages keep saying "invalid token" but we're doing everything correctly according to the guides. I think the problem is in how the API handles refresh tokens, since it seems like tokens expire too quickly. We need to figure out if this behavior is intentional or if there are configuration options we're missing. Has anyone dealt with similar problems? Would appreciate if someone could explain what's the proper way to implement this, because currently our users can barely log in without getting frustrated.

