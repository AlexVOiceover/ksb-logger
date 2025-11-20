Given the following pull request content:
Title: {title}
Body: {body}
Commit Messages: {commit_messages}

Comments: {comments}

And the following KSBs (ONLY USE THESE EXACT IDs):
{ksb_list}

**IMPORTANT: You MUST ONLY use KSB IDs from the list above. Do not create, infer, or suggest any KSB IDs that are not explicitly listed. Each KSB ID in your response must match exactly with one of the IDs provided above.**

Identify which KSB IDs (if any) are relevant to the pull request based on semantic similarity. For each relevant KSB, provide a confidence score (0–100) indicating how well the PR matches the KSB description, using the following criteria:
- 90–100: PR explicitly addresses the KSB with clear, detailed evidence from the title, body, commit messages, diff, or comments.
- 70–89: PR moderately aligns with the KSB, with some relevant terms or partial evidence (e.g., related actions implying the KSB) from the title, body, commit messages, diff, or comments.
- 50–69: PR has weak or indirect alignment, with vague or tangential references from the title, body, commit messages, diff, or comments.
- 0–49: PR has no clear connection or only superficial mentions.
- 0: No relevance to the KSB.

For each relevant KSB, also provide a concise justification (1-2 sentences) explaining how the PR demonstrates the KSB. **Crucially, directly quote or specifically reference relevant lines or sections from the provided Diff or Comments to support your justification.**

Your response should be a JSON object with a single key, `matches`, which is a list of objects. Each object in the `matches` list must have the keys "ksb_id" (string), "score" (integer, 0-100), and "justification" (string). If no KSBs are relevant, return an empty list for `matches`.

**REMINDER: Only use KSB IDs that appear in the list provided above. Using any other KSB ID is strictly forbidden.**