# CHARIS Detection Rules v1.0

**Purpose:** Operational triggers for error detection. Each rule specifies what the system can actually see and when to flag.

**Principle:** Detection is based on **surface patterns**, not learner background. L1 attribution belongs in the explanation layer, not here.

---

## How to Read This Document

Each rule follows this structure:

```yaml
Tag: T2-X-Category:pattern
Trigger: Plain English description
Surface Pattern: What the AI looks for
Detection Logic: Conditions that must be met
Exceptions: When NOT to flag
Catch Examples: Errors this rule should find
Skip Examples: Valid sentences this rule should ignore
```

---

# PART 1: TIER 1 RULES (Mechanical — No Explanation Needed)

## T1-cap

**Trigger:** Missing capitalization at sentence start or on proper nouns

```yaml
Surface Pattern:
  - First character of sentence is lowercase
  - Known proper noun (from NER) is lowercase

Detection Logic:
  - sentence[0].isLower() AND sentence[0] NOT in ['"', "'", "("]
  - entity.type IN [PERSON, PLACE, ORG] AND entity[0].isLower()

Exceptions:
  - Stylistic lowercase (brand names: "iPhone", "eBay")
  - Poetry/creative writing context
  - Code snippets
  - After ellipsis continuation

Catch:
  - "hey Dr. Smith" → "Hey Dr. Smith"
  - "i went to paris" → "I went to Paris"

Skip:
  - "the iPhone works" (brand style)
  - "e.g. this example" (abbreviation)
```

---

## T1-apostrophe

**Trigger:** Missing or incorrect apostrophe in contractions or possessives

```yaml
Surface Pattern:
  - Known contraction spelled without apostrophe
  - Possessive form missing apostrophe
  - Apostrophe in plural (greengrocer's apostrophe)

Detection Logic:
  Contractions (closed list):
    - "dont" → "don't"
    - "cant" → "can't"
    - "wont" → "won't"
    - "isnt" → "isn't"
    - "youre" → "you're"
    - "theyre" → "they're"
    - "its" + [VERB] → "it's" (contraction context)
    - [40+ common contractions]
  
  Possessives:
    - [NOUN] + "s" + [NOUN] where first noun is possessor
    - "the boss desk" → "the boss's desk"

Exceptions:
  - "its" as possessive determiner ("its color")
  - Plural nouns ("the cats sleep")
  - Proper nouns that end in s (style-dependent: "James' book" vs "James's book")

Catch:
  - "dont worry" → "don't worry"
  - "the companys policy" → "the company's policy"
  - "your the best" → "you're the best"

Skip:
  - "its tail" (possessive, not contraction)
  - "the students arrived" (plural, not possessive)
```

---

## T1-typo

**Trigger:** Obvious misspelling with unambiguous correction

```yaml
Surface Pattern:
  - Word not in dictionary
  - Edit distance ≤ 2 from exactly one common word
  - Character transposition, duplication, or omission

Detection Logic:
  - word NOT IN dictionary
  - candidates = words WHERE levenshtein(word, candidate) ≤ 2
  - len(candidates) == 1 OR candidates[0].frequency >> candidates[1].frequency

Exceptions:
  - Proper nouns not in dictionary
  - Technical terms, abbreviations
  - Intentional stylization
  - Multiple equally-likely corrections (→ escalate to T2)

Catch:
  - "teh" → "the"
  - "recieve" → "receive"
  - "occured" → "occurred"
  - "definately" → "definitely"

Skip:
  - "Nguyen" (proper noun)
  - "async" (technical term)
  - "colour/color" (dialect, not error)
```

---

## T1-spacing

**Trigger:** Incorrect spacing around punctuation

```yaml
Surface Pattern:
  - Space before comma, period, colon, semicolon, question mark, exclamation
  - Missing space after comma, period, colon, semicolon
  - Double spaces (unless after period in certain styles)

Detection Logic:
  - /\s[,.:;?!]/ → remove space before
  - /[,.:;?!][^\s\n"]/ → add space after (unless quote/bracket follows)
  - /\s{2,}/ within sentence → reduce to single space

Exceptions:
  - Ellipsis "..."
  - Decimal numbers "3.14"
  - Time format "10:30"
  - URLs and file paths
  - Code snippets

Catch:
  - "Hello , world" → "Hello, world"
  - "Hello,world" → "Hello, world"
  - "end .Start" → "end. Start"

Skip:
  - "e.g." (abbreviation)
  - "3.14159" (number)
  - "http://example.com" (URL)
```

---

## T1-sva (Simple Subject-Verb Agreement)

**Trigger:** Obvious subject-verb number mismatch

```yaml
Surface Pattern:
  - Singular subject + plural verb form
  - Plural subject + singular verb form
  - Simple clause structure (no intervening phrases)

Detection Logic:
  - subject.number != verb.number
  - No complex intervening material between subject and verb
  - Verb is finite (not infinitive, participle, or modal)

Exceptions:
  - Collective nouns (team is/are — both valid)
  - "There is/are" constructions (→ T2)
  - Relative clauses with unclear antecedent (→ T2)
  - Inverted sentences (→ T2)

Catch:
  - "He go to school" → "He goes to school"
  - "The cats runs fast" → "The cats run fast"
  - "She don't know" → "She doesn't know"

Skip:
  - "The team are ready" (BrE collective)
  - "There is many people" (→ T2, dummy subject issue)
  - "The data is/are" (disputed, don't flag)
```

---

## T1-plural-s

**Trigger:** Missing or extra plural -s on obvious count nouns

```yaml
Surface Pattern:
  - Numeric quantifier + singular noun (should be plural)
  - Singular quantifier + plural noun (should be singular)

Detection Logic:
  - [NUMBER > 1] + [NOUN.singular] → flag
  - [NUMBER == 1] + [NOUN.plural] → flag
  - ["many", "several", "few", "multiple"] + [NOUN.singular] → flag
  - ["a", "an", "one", "each", "every"] + [NOUN.plural] → flag

Exceptions:
  - Mass nouns ("two water" → T2, countability issue)
  - Irregular plurals ("two child" → T2-G-IrregularPlural)
  - Compound nouns ("two-year-old")
  - Quantified mass expressions ("two cups of water")

Catch:
  - "three cat" → "three cats"
  - "many student" → "many students"
  - "a books" → "a book"

Skip:
  - "two fish" (irregular plural)
  - "much information" (mass noun)
  - "five-dollar bill" (compound)
```

---

## T1-fragment

**Trigger:** Sentence lacks required main clause components

```yaml
Surface Pattern:
  - No finite verb
  - Subordinate clause only (no main clause)
  - Phrase punctuated as sentence

Detection Logic:
  - Parse tree has no root S node with finite VP
  - Starts with subordinator but no following main clause
  - Contains only NP, PP, or ADJP

Exceptions:
  - Intentional fragments (dialogue, emphasis, creative writing)
  - Headings and titles
  - List items
  - Answers to questions ("When? Tomorrow.")
  - Exclamations ("What a day!")

Catch:
  - "Because I was tired." → fragment (needs main clause)
  - "The big red house on the hill." → fragment (no verb)
  - "Running very fast." → fragment (no finite verb)

Skip:
  - "Fire!" (exclamation)
  - "Project Overview" (heading)
  - "Yes." (valid response)
```

---

## T1-run-on

**Trigger:** Two independent clauses improperly joined

```yaml
Surface Pattern:
  - Two complete sentences joined with only comma (comma splice)
  - Two complete sentences with no punctuation between (fused)

Detection Logic:
  - [S] [,] [S] where both S are independent clauses
  - [S] [S] with no intervening punctuation or conjunction
  - NOT [S] [COORD-CONJ] [S] (that's valid)
  - NOT [S] [;] [S] (that's valid)

Exceptions:
  - Short balanced clauses ("I came, I saw, I conquered")
  - Coordinating conjunction present
  - Semicolon used correctly

Catch:
  - "I went home I was tired" → fused
  - "I went home, I was tired" → comma splice
  - "She runs fast, he walks slow" → comma splice

Skip:
  - "I went home, and I was tired" (conjunction)
  - "I went home; I was tired" (semicolon)
```

---

## T1-article-simple

**Trigger:** Missing article where there is exactly one correct choice

```yaml
Surface Pattern:
  - Ø + singular countable noun in clearly indefinite context
  - First mention, non-specific, profession/role pattern

Detection Logic:
  - [BE/BECOME] + Ø + [SINGULAR-COUNT-NOUN]
  - Noun is clearly indefinite (not previously mentioned, not unique)
  - Only one article makes sense (no a/the ambiguity)

CRITICAL: Escalate to T2 if:
  - Generic reference possible ("Life is hard" vs "A life is hard")
  - Both a/the could work
  - Context needed to determine definiteness

Catch:
  - "She is teacher" → "She is a teacher"
  - "I need pen" → "I need a pen"
  - "He bought car" → "He bought a car"

Skip (→ T2):
  - "I closed door" (could be "the door" — needs context)
  - "Life is hard" (generic — valid without article)
  - "I saw movie" (a movie? the movie? — ambiguous)
```

---

# PART 2: TIER 2-G RULES (Grammar — Explanation Required)

## T2-G-Articles:omission

**Trigger:** Missing article where context determines the correct choice

```yaml
Surface Pattern:
  - Ø + singular countable noun
  - Previous mention or shared knowledge suggests definiteness

Detection Logic:
  - Noun was mentioned earlier → needs "the"
  - Noun is unique in context (the sun, the president) → needs "the"
  - First mention, specific instance → needs "a/an"
  
Context Check:
  - Search prior sentences for same noun/synonym
  - Check for uniqueness markers (superlatives, ordinals)
  - Check for possessive alternatives

Exceptions:
  - Headline style ("Man bites dog")
  - Institutional reference ("go to hospital" in BrE)
  - Fixed phrases ("by car", "at night")

Catch:
  - "I closed door" [context: specific door] → "I closed the door"
  - "She wants to be president" [context: specific role] → context-dependent
  - "Cat is on table" → "The cat is on the table"

Explanation Template:
  "[The/A] is needed because [reason: previous mention / uniqueness / specificity]"
```

---

## T2-G-Articles:overuse

**Trigger:** Article used where none is appropriate

```yaml
Surface Pattern:
  - "the" + generic plural or mass noun
  - Article with abstract noun in generic sense

Detection Logic:
  - "the" + [PLURAL-NOUN] + [GENERIC-PREDICATE]
  - "the" + [MASS-NOUN] in generic statement
  
Generic Indicators:
  - Universal statements ("Ø Dogs are loyal" not "The dogs are loyal")
  - Abstract concepts ("Ø Life is short" not "The life is short")

Exceptions:
  - Specific subset ("The dogs in this park")
  - Cataphoric reference ("The life I lead")

Catch:
  - "The life is hard" → "Life is hard"
  - "The water is essential" → "Water is essential"
  - "I like the music" [generic] → "I like music"

Skip:
  - "The water is cold" (specific water)
  - "The life of Pi" (specific reference)
```

---

## T2-G-Articles:wrong-choice

**Trigger:** Wrong article selected (a ↔ the confusion)

```yaml
Surface Pattern:
  - "a/an" with definite reference
  - "the" with indefinite reference

Detection Logic:
  - Check definiteness: Is referent identifiable to hearer?
    - YES → should be "the"
    - NO → should be "a/an"
  
Definiteness Markers:
  - Previous mention → definite
  - Uniquely identifiable → definite
  - First mention, non-specific → indefinite

Catch:
  - "I saw the movie yesterday. A movie was great." → "The movie was great"
  - "Can you pass a salt?" [unique on table] → "the salt"

Skip:
  - Ambiguous cases where both readings are possible
```

---

## T2-G-Prepositions:substitution

**Trigger:** Wrong preposition for the semantic/syntactic frame

```yaml
Surface Pattern:
  - Verb + preposition combination not in standard frames
  - Adjective + preposition mismatch

Detection Logic:
  Lookup Tables:
    VERB_PREP_FRAMES = {
      "discuss": [Ø],          # NOT "discuss about"
      "explain": ["to"],       # NOT "explain me"
      "depend": ["on"],        # NOT "depend of"
      "different": ["from", "than", "to"],  # NOT "different with"
      "interested": ["in"],    # NOT "interested for"
      ...
    }
  
  - Extract [VERB/ADJ] + [PREP] + [NP]
  - Check if PREP is valid for that VERB/ADJ
  - Flag if not in frame list

Catch:
  - "discuss about the issue" → "discuss the issue"
  - "different with others" → "different from others"
  - "interested for music" → "interested in music"
  - "explain me" → "explain to me"

Skip:
  - Valid alternations ("different from/than/to")
```

---

## T2-G-Prepositions:redundant

**Trigger:** Preposition present where verb takes direct object

```yaml
Surface Pattern:
  - Transitive verb + preposition + object
  - Where verb should take bare NP object

Detection Logic:
  DIRECT_TRANSITIVE = ["enter", "reach", "approach", "contact", "discuss", "mention", "emphasize", ...]
  
  - [VERB in DIRECT_TRANSITIVE] + [PREP] + [NP] → flag

Catch:
  - "enter to the room" → "enter the room"
  - "reach to the goal" → "reach the goal"
  - "contact with him" → "contact him"

Skip:
  - Phrasal verbs where preposition changes meaning
```

---

## T2-G-Prepositions:omission

**Trigger:** Missing required preposition

```yaml
Surface Pattern:
  - Verb requiring prepositional complement lacks it
  - Adjective requiring preposition lacks it

Detection Logic:
  REQUIRES_PREP = {
    "listen": "to",
    "wait": "for",
    "rely": "on",
    "consist": "of",
    ...
  }
  
  - [VERB in REQUIRES_PREP] + [NP] without intervening PREP → flag

Catch:
  - "listen music" → "listen to music"
  - "wait the bus" → "wait for the bus"

Skip:
  - Ellipsis in informal speech where acceptable
```

---

## T2-G-TenseAspect:tense-adverb-conflict

**Trigger:** Verb tense contradicts temporal adverbial

```yaml
Surface Pattern:
  - Present perfect + specific past time
  - Simple past + "since" or current relevance marker
  - Future + past time adverb

Detection Logic:
  CONFLICTS = [
    (PRESENT_PERFECT, ["yesterday", "last week", "in 1990", "ago"]),
    (SIMPLE_PAST, ["since", "so far", "up to now", "recently" + current relevance]),
    (FUTURE, ["yesterday", "last", "ago"]),
  ]
  
  - Parse tense of main verb
  - Extract temporal adverbials
  - Check for conflict patterns

Catch:
  - "I have seen him yesterday" → "I saw him yesterday"
  - "I lived here since 2010" → "I have lived here since 2010"
  - "I will go yesterday" → logical error

Skip:
  - "I have seen him recently" (valid)
  - "I saw him since-deleted emails" (different "since")
```

---

## T2-G-TenseAspect:stative-progressive

**Trigger:** Progressive aspect with stative verb

```yaml
Surface Pattern:
  - BE + VERB-ing where verb is stative

Detection Logic:
  STATIVE_VERBS = ["know", "believe", "understand", "want", "need", "like", "love", 
                  "hate", "prefer", "belong", "own", "possess", "contain", "consist",
                  "seem", "appear", "mean", "matter", ...]
  
  - [BE] + [STATIVE_VERB + ing] → flag
  
  BUT CHECK: Some statives allow progressive in specific meanings:
    - "I'm thinking" (active thought process — OK)
    - "I'm seeing someone" (dating — OK)
    - "I'm having dinner" (eating — OK)

Catch:
  - "I am knowing the answer" → "I know the answer"
  - "She is believing him" → "She believes him"
  - "I am owning a car" → "I own a car"

Skip:
  - "I'm thinking about it" (valid — active process)
  - "I'm having a good time" (valid — experience)
  - "He's being difficult" (valid — temporary behavior)
```

---

## T2-G-TenseAspect:sequence-error

**Trigger:** Inconsistent tense within narrative or logical sequence

```yaml
Surface Pattern:
  - Tense shift without temporal shift
  - Past narrative with random present intrusion
  - Reporting verbs with wrong backshift

Detection Logic:
  - Track tense across sentence boundaries
  - Flag unmotivated shifts
  - Check reported speech backshift rules

Catch:
  - "I went to the store. I buy milk." → "I bought milk"
  - "He said he is tired" [past reporting] → "He said he was tired"
  - "When I arrived, he leaves" → "he left" or "he had left"

Skip:
  - Historical present (deliberate narrative device)
  - Direct quotation
  - General truths in past narrative ("He said the earth is round")
```

---

## T2-G-Countability:plural-mass

**Trigger:** Plural marking on uncountable noun

```yaml
Surface Pattern:
  - Mass noun + plural -s
  - Mass noun with "many" or count quantifier

Detection Logic:
  MASS_NOUNS = ["equipment", "furniture", "information", "advice", "news", 
               "research", "knowledge", "luggage", "baggage", "homework",
               "evidence", "progress", "traffic", "weather", ...]
  
  - [MASS_NOUN] + plural morpheme → flag
  - "many" + [MASS_NOUN] → flag

Catch:
  - "equipments" → "equipment"
  - "furnitures" → "furniture"
  - "many informations" → "much information"
  - "an advice" → "a piece of advice"

Skip:
  - Countable uses ("different weathers" in technical contexts)
  - Proper count nouns that look mass ("researches" as noun — rare but attested)
```

---

## T2-G-Countability:det-noun-mismatch

**Trigger:** Determiner number doesn't match noun number

```yaml
Surface Pattern:
  - Singular determiner + plural noun
  - Plural determiner + singular noun

Detection Logic:
  SINGULAR_DET = ["this", "that", "a", "an", "each", "every"]
  PLURAL_DET = ["these", "those", "many", "few", "several"]
  
  - [SINGULAR_DET] + [PLURAL_NOUN] → flag
  - [PLURAL_DET] + [SINGULAR_NOUN] → flag

Catch:
  - "this books" → "this book" or "these books"
  - "these information" → "this information"
  - "many student" → "many students"

Skip:
  - Mass nouns with "this/that" ("this information")
```

---

## T2-G-Countability:quantifier-error

**Trigger:** Wrong quantifier for noun's countability

```yaml
Surface Pattern:
  - "much" + countable noun
  - "many" + uncountable noun
  - "less" + countable noun (prescriptive rule)
  - "fewer" + uncountable noun

Detection Logic:
  - "much" + [COUNT_NOUN] → flag ("much books" → "many books")
  - "many" + [MASS_NOUN] → flag ("many information" → "much information")
  - "less" + [COUNT_NOUN.plural] → flag if strictness=high

Catch:
  - "much people" → "many people"
  - "less problems" → "fewer problems" (prescriptive)

Skip:
  - "less" + count noun in informal (if strictness ≠ high)
```

---

## T2-G-IrregularPlural:over-regularization

**Trigger:** Regular -s/-es applied to irregular plural noun

```yaml
Surface Pattern:
  - Irregular noun with regular plural ending

Detection Logic:
  IRREGULAR_PLURALS = {
    "child": "children",    # NOT "childs"
    "man": "men",           # NOT "mans"
    "woman": "women",       # NOT "womans"
    "foot": "feet",         # NOT "foots"
    "tooth": "teeth",       # NOT "tooths"
    "mouse": "mice",        # NOT "mouses"
    "person": "people",     # NOT "persons" (usually)
    "goose": "geese",       # NOT "gooses"
    ...
  }
  
  - [IRREGULAR_NOUN + regular plural ending] → flag

Catch:
  - "childs" → "children"
  - "mouses" → "mice"
  - "womans" → "women"
  - "tooths" → "teeth"

Skip:
  - "persons" (legal/formal contexts)
  - "mouses" (computer devices — disputed)
```

---

## T2-G-Transitivity:valency-frame

**Trigger:** Verb used with wrong complement structure

```yaml
Surface Pattern:
  - Verb complement doesn't match expected frame

Detection Logic:
  VALENCY_FRAMES = {
    "suggest": ["that-clause", "NP", "V-ing"],    # NOT "suggest to-inf" or "suggest NP to-inf"
    "recommend": ["that-clause", "NP", "V-ing"], # NOT "recommend NP to-inf"
    "explain": ["NP to NP", "that-clause"],      # NOT "explain NP NP"
    "say": ["that-clause", "NP to NP"],          # NOT "say NP that"
    ...
  }
  
  - Parse complement structure
  - Check against valency frame
  - Flag mismatches

Catch:
  - "He suggested me to go" → "He suggested that I go" / "He suggested I go"
  - "She explained me the problem" → "She explained the problem to me"
  - "I recommend you to try" → "I recommend that you try"

Skip:
  - Valid alternations
```

---

## T2-G-DummySubject:omission

**Trigger:** Missing expletive "it" or "there"

```yaml
Surface Pattern:
  - Weather/time expression without "it"
  - Existential without "there"
  - Extraposed subject without "it"

Detection Logic:
  - [BE/SEEM] + [ADJECTIVE] + [to-clause/that-clause] without preceding "it"
  - Weather verbs without subject
  - Existential pattern without "there"

Catch:
  - "Is raining" → "It is raining"
  - "Is a problem" → "There is a problem"
  - "Is important to study" → "It is important to study"
  - "Seems that he left" → "It seems that he left"

Skip:
  - Imperatives
  - Informal diary style
```

---

## T2-G-DummySubject:wrong-choice

**Trigger:** "It" ↔ "there" confusion

```yaml
Surface Pattern:
  - "There" in non-existential context
  - "It" in existential context

Detection Logic:
  - Existential (introduces existence/presence) → "there"
  - Weather, time, extraposition → "it"

Catch:
  - "It has a problem" [existential meaning] → "There is a problem"
  - "There is raining" → "It is raining"
  - "There seems important" → "It seems important"

Skip:
  - Ambiguous cases
```

---

## T2-G-WordForm:pos-shift

**Trigger:** Wrong part of speech used in syntactic slot

```yaml
Surface Pattern:
  - Noun where adjective needed
  - Adjective where adverb needed
  - Verb where noun needed

Detection Logic:
  - [DETERMINER] + [VERB/ADJ used as noun] → flag
  - [VERB] + [ADJ instead of ADV] → flag
  - [BE] + [NOUN instead of ADJ] → flag

Catch:
  - "She made a decide" → "She made a decision"
  - "He runs quick" → "He runs quickly"
  - "It was a beauty day" → "It was a beautiful day"

Skip:
  - Conversion where established ("a run", "a find")
  - Flat adverbs ("drive fast", "work hard")
```

---

## T2-G-WordForm:derivation-error

**Trigger:** Non-existent or malformed derived word

```yaml
Surface Pattern:
  - Verb with wrong past tense/participle formation
  - Non-existent derivational form

Detection Logic:
  - Word not in dictionary
  - Apparent derivation attempt from known root
  - Single clear correction exists

Catch:
  - "successed" → "succeeded"
  - "informations" → "information"
  - "beautifulity" → "beauty"
  - "suggestly" → "suggestively" or rephrase

Skip:
  - Neologisms in appropriate context
  - Technical jargon
```

---

## T2-G-Comparatives:double-marker

**Trigger:** Both inflectional and periphrastic comparison used

```yaml
Surface Pattern:
  - "more" + adjective with -er
  - "most" + adjective with -est

Detection Logic:
  - "more" + [ADJ ending in -er] → flag
  - "most" + [ADJ ending in -est] → flag

Catch:
  - "more better" → "better"
  - "most fastest" → "fastest"
  - "more easier" → "easier"

Skip:
  - "more and more" (intensifier)
```

---

## T2-G-Comparatives:connector-error

**Trigger:** Wrong word in comparison structure

```yaml
Surface Pattern:
  - "as...than" instead of "as...as"
  - "more...as" instead of "more...than"

Detection Logic:
  - "as" + [ADJ/ADV] + "than" → flag (should be "as...as")
  - [COMPARATIVE] + "as" → flag (should be "than")

Catch:
  - "as tall than him" → "as tall as him"
  - "more tall as him" → "taller than him"

Skip:
  - "not so much X as Y" (valid construction)
```

---

## T2-G-ClauseStructure:subordination-error

**Trigger:** Malformed subordinate clause, including missing subjunctive

```yaml
Surface Pattern:
  - Mandative verb/adjective + indicative instead of subjunctive
  - Double conjunction
  - Missing subordinator

Detection Logic:
  MANDATIVE_TRIGGERS = ["suggest", "recommend", "propose", "insist", "demand",
                        "important", "essential", "necessary", "vital"]
  
  - [MANDATIVE] + "that" + [3sg verb with -s] → flag (should be base form)
  
  DOUBLE_CONJUNCTION = ["because...so", "although...but", "if...then...so"]
  - Flag redundant conjunction in pair

Catch:
  - "I suggest that he goes" → "I suggest that he go"
  - "Because he was late, so we left" → remove "so"
  - "Although it rained, but we went" → remove "but"

Skip:
  - BrE "suggest that he should go" (valid alternative)
  - "If X, then Y" (then optional but valid)
```

---

# PART 3: TIER 2-N RULES (Naturalness — Explanation Required)

## T2-N-Collocation:verb-noun

**Trigger:** Non-native verb + noun pairing

```yaml
Surface Pattern:
  - Verb + object noun combination with low corpus frequency

Detection Logic:
  COLLOCATION_LOOKUP = {
    # Format: (wrong_verb, noun) → correct_verb
    ("do", "mistake"): "make",
    ("make", "homework"): "do",
    ("do", "photo"): "take",
    ("make", "research"): "conduct/do",
    ...
  }
  
  Method:
  1. Extract [VERB] + [direct object NOUN]
  2. Lookup in COLLOCATION_LOOKUP for known errors
  3. OR compute MI/t-score from reference corpus
  4. Flag if MI < 3.0 or not in top-10 collocates

Catch:
  - "do a mistake" → "make a mistake"
  - "make homework" → "do homework"
  - "make a photo" → "take a photo"

Skip:
  - Creative/intentional variations
  - Domain-specific usage
```

---

## T2-N-Collocation:verb-particle

**Trigger:** Non-idiomatic verb + particle combination for device/appliance control

```yaml
Surface Pattern:
  - Literal translation of L1 verb for turning on/off

Detection Logic:
  DEVICE_VERBS = {
    # Common L1 transfer patterns
    ("open", ["light", "TV", "computer", "AC", "fan"]): "turn on",
    ("close", ["light", "TV", "computer", "AC", "fan"]): "turn off",
    ("open", ["radio"]): "turn on",
    ("close", ["radio"]): "turn off",
  }
  
  - [VERB] + [DEVICE_NOUN] → check against DEVICE_VERBS
  - Flag if verb is "open/close" with electrical device

Catch:
  - "open the light" → "turn on the light"
  - "close the TV" → "turn off the TV"
  - "open the AC" → "turn on the AC"

Skip:
  - "open the laptop" (physically opening — valid)
  - "close the laptop" (physically closing — valid)
```

---

## T2-N-Collocation:adj-noun

**Trigger:** Non-native adjective + noun pairing

```yaml
Surface Pattern:
  - Adjective + noun with low corpus frequency relative to alternatives

Detection Logic:
  ADJ_NOUN_LOOKUP = {
    ("heavy", "taste"): "strong",
    ("big", "rain"): "heavy",
    ("strong", "cold"): "bad/severe",
    ...
  }
  
  Method:
  1. Extract [ADJ] + [NOUN] pairs
  2. Check against known non-native patterns
  3. OR compare corpus frequency with synonymous adjectives

Catch:
  - "heavy taste" → "strong taste"
  - "big rain" → "heavy rain"

Skip:
  - Creative/poetic usage
  - Technical terms
```

---

## T2-N-WordOrder:adverb-placement

**Trigger:** Adverb in non-native position

```yaml
Surface Pattern:
  - Adverb between subject and verb where post-verb is standard
  - Degree adverb before verb instead of after

Detection Logic:
  - "I very like" → "I like very much" / "I really like"
  - "She always is" → "She is always"
  - [SUBJ] [DEGREE_ADV] [VERB] → flag if degree adverb

Common Patterns:
  - "very" directly before main verb (without auxiliary)
  - "always/never" after main verb BE
  - Frequency adverbs after lexical verb (non-native position)

Catch:
  - "I very like it" → "I like it very much"
  - "She always is late" → "She is always late"
  - "I yesterday went" → "I went yesterday" / "Yesterday I went"

Skip:
  - Fronted adverbs for emphasis ("Never have I seen...")
  - Mid-position with auxiliaries ("I have always liked")
```

---

## T2-N-WordOrder:topicalization

**Trigger:** Non-native topic-fronting without appropriate marking

```yaml
Surface Pattern:
  - Object NP before subject-verb without focus/contrast marking
  - L1-influenced topic-comment structure

Detection Logic:
  - [OBJECT NP] [SUBJECT] [VERB] without:
    - Contrastive stress context
    - "As for" / "Regarding" marker
    - Relative clause structure
  - No clear discourse motivation for fronting

Catch:
  - "This book I read yesterday" → "I read this book yesterday"
  - "That problem we will discuss later" → "We will discuss that problem later"

Skip:
  - Contrastive topicalization ("This one I like, that one I don't")
  - Relative clauses ("the book that I read")
```

---

## T2-N-Register:formality-clash

**Trigger:** Mixed formality levels within same text

```yaml
Surface Pattern:
  - Formal vocabulary/structure mixed with informal
  - Slang in formal context or vice versa

Detection Logic:
  FORMAL_MARKERS = ["hereby", "aforementioned", "pursuant to", "endeavour", ...]
  INFORMAL_MARKERS = ["gonna", "wanna", "kinda", "hey", "dude", "cool", ...]
  
  Method:
  1. Score each sentence for formality (lexical + structural)
  2. Calculate variance across text
  3. Flag if variance > threshold (large stylistic jumps)
  4. Flag specific clashes (formal + informal in same sentence)

Catch:
  - "I hereby wanna inform you" → clash
  - "Hey Professor, I would be most grateful" → clash
  - "The aforementioned dude" → clash

Skip:
  - Intentional code-switching
  - Quotations
```

---

## T2-N-Cohesion:redundant-linker

**Trigger:** Paired conjunctions where only one is needed

```yaml
Surface Pattern:
  - "because...so"
  - "although...but"
  - "if...then...so"
  - "the reason is because"

Detection Logic:
  REDUNDANT_PAIRS = [
    (r"[Bb]ecause .+, so", "remove 'so'"),
    (r"[Aa]lthough .+, but", "remove 'but'"),
    (r"[Tt]he reason .+ is because", "use 'The reason is that' or 'because'"),
    (r"[Tt]he reason why .+ is because", "use 'The reason is that'"),
  ]
  
  - Match patterns and flag

Catch:
  - "Because he was late, so we left" → "Because he was late, we left"
  - "Although it rained, but we went" → "Although it rained, we went"
  - "The reason is because I'm tired" → "The reason is that I'm tired"

Skip:
  - "If X, then Y" (then is optional but not redundant)
```

---

## T2-N-Cohesion:connector-misuse

**Trigger:** Wrong logical connector for the semantic relationship

```yaml
Surface Pattern:
  - Connector doesn't match logical relationship between clauses

Detection Logic:
  Check semantic relationship:
  - CONTRAST: but, however, although, despite
  - CAUSE: because, since, as
  - RESULT: so, therefore, thus, hence
  - ADDITION: and, also, moreover, furthermore
  
  Flag if connector type doesn't match clause relationship
  
  Common Errors:
  - "In the other side" → "On the other hand"
  - "In the other hand" → "On the other hand"
  - "In contrast" used for addition

Catch:
  - "In the other side" → "On the other hand"
  - "He was tired, moreover he went home" [result, not addition] → "therefore"
  - "Despite he was sick" → "Despite being sick" / "Although he was sick"

Skip:
  - Valid connector use even if alternative exists
```

---

## T2-N-Idiomaticity:literal-transfer

**Trigger:** Literally translated L1 idiom or expression

```yaml
Surface Pattern:
  - Phrase that matches literal translation of known L1 idiom

Detection Logic:
  LITERAL_TRANSFERS = {
    # Cantonese → English literal translations
    "add oil": "keep going / good luck",
    "people mountain people sea": "very crowded",
    "no eye see": "can't bear to watch",
    "give face": "show respect",
    ...
    
    # More general ESL patterns
    "according to me": "in my opinion",
    "discuss about": "discuss",
  }
  
  - Match against known literal transfer patterns
  - Flag with idiomatic alternative

Catch:
  - "according to me" → "in my opinion"
  - Context-dependent transfer patterns

Skip:
  - Established borrowings
  - Intentional cultural reference
```

---

## T2-N-StructureBridge:grammatical-unnatural

**Trigger:** Grammatically valid but low-frequency native construction

```yaml
Surface Pattern:
  - Parses correctly
  - Very low frequency in native corpus
  - Native speaker would phrase differently

Detection Logic:
  Method:
  1. Sentence parses without error
  2. Check construction frequency in reference corpus
  3. If frequency < threshold AND clear alternative exists → flag
  
  Patterns:
  - "Is better you come" → "It's better if you come"
  - "I have ever been there" [positive polarity] → "I have been there before"
  - "He is a very good friend of me" → "of mine"

Catch:
  - "Is better you come" → "It's better if you come"
  - "a friend of me" → "a friend of mine"

Skip:
  - Rare but established constructions
  - Formal/literary variants
```

---

# PART 4: THRESHOLDS AND CONFIGURATION

## Strictness Settings

```yaml
LOW:
  - Flag only clear errors
  - Collocation MI threshold: < 1.5
  - Skip prescriptive-only rules (less/fewer)
  - Skip register variance < 3σ
  - Skip low-frequency but grammatical constructions

MEDIUM (default):
  - Flag clear errors + common naturalness issues
  - Collocation MI threshold: < 3.0
  - Include prescriptive rules marked "common"
  - Flag register variance > 2σ
  - Flag constructions below 5th percentile frequency

HIGH:
  - Flag everything above + marginal cases
  - Collocation MI threshold: < 4.0
  - Include all prescriptive rules
  - Flag register variance > 1.5σ
  - Flag constructions below 15th percentile frequency
```

---

## Dialect Handling

```yaml
AmE (default):
  - "gotten" = valid
  - "dove" (past of dive) = valid
  - "toward" preferred over "towards"
  - Collective nouns usually singular

BrE:
  - "got" preferred over "gotten"
  - "dived" preferred over "dove"
  - "towards" preferred
  - Collective nouns often plural ("the team are")
  - "at hospital" (no article) = valid

Cross-dialect:
  - Never flag spelling differences (color/colour)
  - Never flag both valid forms
  - Only flag if inconsistent WITHIN document
```

---

## Reference Corpus Baselines

```yaml
Collocation Scoring:
  - Source: COCA, BNC, or combined
  - Metric: Mutual Information (MI) or t-score
  - Threshold varies by strictness

Construction Frequency:
  - Source: COCA/BNC syntactic patterns
  - Percentile-based flagging

Register Scoring:
  - Formality lexicon (academic word list, slang list)
  - Sentence-level formality score
  - Document variance calculation
```

---

# APPENDIX: Pattern Lookup Tables

## A. Mass Nouns (Uncountable)

```
equipment, furniture, information, advice, news, research, knowledge,
luggage, baggage, homework, evidence, progress, traffic, weather,
accommodation, behavior, bread, cash, clothing, content, damage,
electricity, feedback, food, fruit, garbage, hair, happiness, health,
help, importance, jewelry, justice, laughter, leisure, luck, machinery,
mail, money, music, nonsense, paper, patience, permission, pollution,
poverty, produce, rain, rubbish, safety, sand, scenery, shopping,
significance, snow, software, stuff, thunder, transportation, trash,
violence, vocabulary, water, wealth, wildlife, work
```

## B. Irregular Plurals

```
child → children       man → men           woman → women
foot → feet            tooth → teeth       goose → geese
mouse → mice           louse → lice        ox → oxen
person → people        die → dice          penny → pence (BrE)
sheep → sheep          deer → deer         fish → fish
species → species      series → series     aircraft → aircraft
```

## C. Stative Verbs

```
MENTAL: know, believe, understand, recognize, realize, suppose, imagine,
        doubt, remember, forget, mean, want, need, prefer, agree,
        disagree, deny, promise, satisfy

EMOTIONAL: like, love, hate, dislike, fear, envy, mind, care, wish,
           hope, desire, appreciate, value

POSSESSION: have, own, possess, belong, contain, consist, include,
            lack, owe

PERCEPTION: see, hear, smell, taste, feel, notice, observe

RELATIONAL: be, seem, appear, look, sound, resemble, equal, fit,
            depend, matter, weigh, cost, measure
```

## D. Mandative Verbs/Adjectives (Require Subjunctive)

```
VERBS: suggest, recommend, propose, insist, demand, request, require,
       ask, advise, urge, prefer, command, order, decree

ADJECTIVES: important, essential, necessary, vital, crucial, imperative,
            advisable, desirable, preferable, urgent, critical
```

## E. Verb Valency Frames (Partial)

```yaml
explain:
  - [NP] to [NP]        # explain the problem to me
  - [that-clause]       # explain that it was wrong
  - [wh-clause]         # explain why it happened
  - NOT: [NP] [NP]      # *explain me the problem

suggest:
  - [that-clause]       # suggest that we leave
  - [NP]                # suggest a solution
  - [V-ing]             # suggest leaving
  - NOT: [NP to-inf]    # *suggest me to leave

recommend:
  - [that-clause]       # recommend that he go
  - [NP]                # recommend a book
  - [V-ing]             # recommend reading
  - NOT: [NP to-inf]    # *recommend you to try

discuss:
  - [NP]                # discuss the issue
  - NOT: [about NP]     # *discuss about the issue
```

---

# Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2025-01-30 | Initial detection rules specification |
