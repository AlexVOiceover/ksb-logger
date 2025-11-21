# Evidence Quality Assessment

You are evaluating multiple pull requests that have been matched to a specific KSB (Knowledge, Skill, or Behaviour). Your task is to rank these PRs by evidence quality to identify which one provides the BEST demonstration of the KSB.

## Input Data

**KSB ID:** {ksb_id}
**KSB Description:** {ksb_description}
**KSB Type:** {ksb_type} (Knowledge, Skill, or Behaviour)

**Matched Pull Requests:**
{pr_list}

## Evidence Quality Criteria

Assess each PR against these criteria (score each 0-10):

### 1. **Depth of Evidence**
- **High (8-10)**: Multiple detailed examples, extensive code changes, thorough documentation
- **Medium (4-7)**: Some detail, moderate code changes, basic documentation
- **Low (0-3)**: Superficial mentions, minimal changes, no supporting detail

### 2. **Technical Complexity**
- **High (8-10)**: Complex problem-solving, architectural decisions, multiple technologies
- **Medium (4-7)**: Moderate technical challenge, straightforward implementation
- **Low (0-3)**: Trivial changes, simple fixes, no technical depth

### 3. **Scope of Impact**
- **High (8-10)**: System-wide changes, affects multiple components, significant user impact
- **Medium (4-7)**: Module-level changes, affects one component, moderate impact
- **Low (0-3)**: Isolated changes, minimal impact, no broader implications

### 4. **Evidence Clarity**
- **High (8-10)**: Clear commit messages, detailed PR description, comprehensive diff, helpful comments
- **Medium (4-7)**: Adequate description, understandable changes, some documentation
- **Low (0-3)**: Vague descriptions, unclear changes, missing context

### 5. **KSB Alignment**
- **High (8-10)**: Direct, explicit demonstration of the KSB with multiple supporting examples
- **Medium (4-7)**: Clear connection to KSB, some supporting evidence
- **Low (0-3)**: Tangential or implied connection, weak supporting evidence

### 6. **Maturity Indicator** (for Skills and Behaviours)
- **High (8-10)**: Shows independent decision-making, proactive problem-solving, lessons learned
- **Medium (4-7)**: Competent execution, follows guidance, basic reflection
- **Low (0-3)**: Basic task completion, no reflection, minimal independence

### 7. **Context Richness**
- **High (8-10)**: Clear business context, user impact explained, trade-offs discussed
- **Medium (4-7)**: Some context provided, basic rationale given
- **Low (0-3)**: No context, purely technical changes, missing "why"

## Special Considerations by KSB Type

### For Knowledge KSBs (K-prefix)
- Prioritize PRs that demonstrate **understanding** through decisions, not just application
- Look for evidence of choosing between alternatives with rationale
- Value explanations in PR descriptions and comments

### For Skills KSBs (S-prefix)
- Prioritize PRs showing **practical application** with tangible outputs
- Look for evidence of following established practices/frameworks
- Value code quality, test coverage, and technical execution

### For Behaviour KSBs (B-prefix)
- Prioritize PRs showing **patterns of professional conduct**
- Look for collaboration evidence (reviews, discussions, teamwork)
- Value reflection, communication, and growth mindset indicators

## Recency Weighting

When scores are similar (within 5 points), prefer more recent PRs as they show:
- Current skill level (not historical)
- Growth and learning over time
- More mature approach to problems

However, DO NOT automatically prefer recent over significantly better older evidence.

## Output Format

Return a JSON object with the following structure:

```json
{
  "ranked_prs": [
    {
      "pr_url": "<url>",
      "pr_title": "<title>",
      "pr_date": "<date>",
      "total_score": <0-70>,
      "criteria_scores": {
        "depth": <0-10>,
        "complexity": <0-10>,
        "impact": <0-10>,
        "clarity": <0-10>,
        "alignment": <0-10>,
        "maturity": <0-10>,
        "context": <0-10>
      },
      "ranking_justification": "<2-3 sentences explaining why this PR ranked where it did, highlighting strengths and weaknesses>",
      "evidence_highlights": [
        "<specific quote or reference from diff/comments>",
        "<another specific example>"
      ]
    }
  ],
  "recommendation": {
    "selected_pr_url": "<url of highest ranked PR>",
    "rationale": "<2-3 sentences explaining why this is the best evidence for the KSB>",
    "alternative_use": "<optional: if the second-ranked PR has unique value, suggest how it might supplement the primary evidence>"
  }
}
```

## Important Notes

- **Be discriminating**: Not all matched PRs are good evidence. Low scores are acceptable and helpful.
- **Quote specifically**: Include actual text from diff, commit messages, or comments in evidence_highlights
- **Consider the assessor**: Choose evidence that will be easy for an external assessor to verify and understand
- **Minimum threshold**: PRs scoring below 35/70 total are likely insufficient as primary evidence
