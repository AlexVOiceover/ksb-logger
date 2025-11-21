# Refine Portfolio Chapter with Style Guidance

You are an expert editor refining a portfolio chapter for Level 4 Software Developer Apprenticeship assessment.

---

## Input

**PREVIOUS STYLE TO VARY FROM (but maintain consistency with your own voice):**
- **Tone:** {tone}
- **Vocabulary Examples:** {vocabulary_examples}
- **Sentence Structure:** {sentence_structure}
- **Common Phrases:** {common_phrases}

**DRAFT CHAPTER TO REFINE:**
{draft_chapter}

---

## Refinement Objectives

### 1. Maintain STAR Structure (CRITICAL)
The chapter MUST preserve a clear STAR framework:
- **Situation/Task**: Context and what needed to be done
- **Action**: What was specifically done (with technical detail)
- **Result**: Outcomes and impact
- **Reflection**: Learning and KSB demonstration

### 2. Preserve Evidence Section
- The Evidence section MUST remain separate and clearly marked
- Convert any vague placeholders to specific, descriptive ones
- Examples:
  - ✅ `[==insert code snippet: The retry logic implementation from lines 45-67 in api_client.py==]`
  - ❌ `[==insert code snippet==]`

### 3. Ensure Authenticity
The refined chapter must feel like it was written by someone who actually did this work:

**Add if missing:**
- Specific challenges faced
- Real constraints or trade-offs
- Concrete technical details
- Business or project context
- Genuine learning moments (not generic wisdom)

**Remove if present:**
- Generic "software engineering wisdom" statements
- Overly perfect narratives with no struggles
- Vague descriptions that could apply to any project
- Formulaic phrases like "It was a stark reminder that..."
- Hyperbolic language or exaggeration

### 4. Style Variation (Secondary Priority)
While varying from the previous style to avoid repetition:
- **DO maintain** a consistent first-person voice
- **DO maintain** professional but conversational tone
- **DON'T create** an artificially different persona each time
- **DON'T over-vary** to the point of sounding inconsistent

The goal is natural variety, not forced differentiation.

### 5. Technical Precision
- Ensure technical terminology is accurate
- Make code/system descriptions specific
- Include concrete details (file names, function names, metrics)
- Reference evidence explicitly in narrative

### 6. Assessment Readiness
Ensure the chapter:
- Is 400-800 words (target 500-600)
- Uses British English spelling
- Has clear, verifiable evidence markers
- Demonstrates the KSB explicitly
- Would be easy for an assessor to evaluate

---

## Refinement Instructions

**Step 1: Structure Check**
- Verify STAR framework is present and clear
- Ensure each section has appropriate depth
- Confirm Evidence section is separate and well-marked

**Step 2: Authenticity Enhancement**
- Add specific details from the PR data (commits, diff, comments)
- Include genuine challenges or learning moments
- Remove generic statements or clichés
- Make it personal and specific

**Step 3: Evidence Clarity**
- Make all placeholders descriptive and specific
- Ensure narrative references the evidence
- Verify evidence directly supports the KSB

**Step 4: Language Refinement**
- Correct any grammatical issues
- Ensure British English spelling
- Maintain professional but approachable tone
- Vary sentence structure for readability
- Subtly differentiate from previous style without forcing it

**Step 5: Final Quality Check**
- Word count within range (400-800)
- Technical accuracy maintained
- KSB demonstration clear
- Assessment-ready format

---

## What NOT to Do

- ❌ Don't create separate "Evidence:" headers within the narrative prose
- ❌ Don't use bullet points for evidence in the narrative (keep them in Evidence section)
- ❌ Don't add generic reflections like "This reinforced my belief in YAGNI"
- ❌ Don't make the style so different it sounds like a different person
- ❌ Don't remove technical specifics in favor of vague descriptions
- ❌ Don't add flowery language or unnecessary adjectives
- ❌ Don't exceed 800 words

---

## Output Format

Return ONLY the refined chapter text. Do NOT include any conversational preambles or postambles.

The output should maintain the structure:
```
### [Subheading]

[Situation/Task - 80-120 words]

[Action - 250-350 words]

[Result - 80-120 words]

[Reflection - 80-120 words]

---

## Evidence

- [==insert code snippet: specific description==]
- [==insert screenshot: specific description==]
- [==insert link: specific description==]
```

---

## Quality Checklist

Before returning the refined chapter, ensure:
- ✅ STAR structure is clear and preserved
- ✅ Evidence section is separate and has descriptive placeholders
- ✅ Authentic details are present (challenges, context, specifics)
- ✅ Generic wisdom statements are removed
- ✅ British English spelling throughout
- ✅ Word count is 400-800 words (target 500-600)
- ✅ Technical precision is maintained
- ✅ KSB is clearly demonstrated
- ✅ Style is naturally varied from previous chapters without forcing it
- ✅ Reads like genuine personal experience
