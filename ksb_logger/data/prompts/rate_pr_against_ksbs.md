Given the following pull request content:
Title: {title}
Body: {body}
Commit Messages: {commit_messages}
Diff: {diff}
Comments: {comments}

And the following KSBs (ONLY USE THESE EXACT IDs):
{ksb_list}

**IMPORTANT: You MUST ONLY use KSB IDs from the list above. Do not create, infer, or suggest any KSB IDs that are not explicitly listed. Each KSB ID in your response must match exactly with one of the IDs provided above.**

Identify which KSB IDs (if any) are relevant to the pull request based on BOTH semantic similarity AND evidence quality. For each relevant KSB, provide a confidence score (0–100) indicating how well the PR demonstrates the KSB, using the following criteria:

**Scoring Criteria:**

- **90–100** (Exceptional Evidence):
  - PR explicitly addresses the KSB with clear, detailed evidence
  - Multiple supporting examples from diff, commits, or comments
  - Shows depth of understanding/skill (not just surface-level)
  - Technical complexity appropriate to demonstrate the KSB
  - Clear business context or impact described

- **70–89** (Strong Evidence):
  - PR clearly aligns with the KSB with good supporting evidence
  - Some detail in diff or description showing competency
  - Adequate technical depth for the KSB
  - Some context provided

- **50–69** (Weak Evidence):
  - PR has indirect alignment or partial evidence
  - Vague or tangential references
  - Limited technical depth
  - Missing context or rationale

- **Below 50** (Insufficient):
  - PR has superficial mentions or no clear connection
  - Inadequate evidence to demonstrate the KSB
  - **Do not include in results** (only return KSBs scoring 50+)

For each relevant KSB, also provide a concise justification (1-2 sentences) explaining how the PR demonstrates the KSB. **Crucially, directly quote or specifically reference relevant lines or sections from the provided Diff or Comments to support your justification.**

Your response should be a JSON object with a single key, `matches`, which is a list of objects. Each object in the `matches` list must have the keys "ksb_id" (string), "score" (integer, 50-100), and "justification" (string).

**IMPORTANT NOTES:**
- Only include KSBs with scores of 50 or higher
- If no KSBs meet the 50+ threshold, return an empty list for `matches`
- Only use KSB IDs that appear in the list provided above
- Be selective: not every PR demonstrates every KSB it mentions