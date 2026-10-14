---
name: lock-it-in
description: 'Save a decision the user just made into one decisions file, dated and in their exact words, so every future chat reads it first and never re-argues it. Use when the user says "lock it in", "that is final", "remember this", "we decided", or settles a price, name, rule or plan. Also read the decisions file at the start of any task it might affect.'
---

# lock-it-in: decide once, and every chat remembers

Claude forgets. You settle a price or a name in one chat and the next chat has no idea, or argues with you about it. This skill keeps one file of everything you decided, and makes every chat read it before it answers.

## The file
One file: `DECISIONS.md` in the project root (or the folder the user names). Create it if it does not exist, with this at the top:

```
# Decisions
Read this before answering anything it covers. Newest entries at the bottom.
Next ID: D-001
```

## When the user says "lock it in"
1. **Find what they decided.** Take the decision from the conversation. If it is unclear what exactly is being locked, ask one short question.
2. **Use their exact words.** Quote the sentence where they decided it. Do not paraphrase it into something cleaner.
3. **Check for a clash.** Search the file for anything on the same topic. If an older entry says something different, show both and ask: "This replaces D-007, right?" Never silently keep both.
4. **Write the entry** using the next ID, then bump the Next ID line in the same edit:

```
## D-012 · 2026-03-04 · Pricing
Decision: Starter plan is $49 a month.
Their words: "lock it in, 49 a month for starter, not 39"
Replaces: D-007
Applies to: pricing page, proposals, emails
```

5. **If it replaces an older one,** add `Replaced by D-012` under the old entry. Never delete old entries.
6. **Confirm in one line:** "Locked as D-012."

## At the start of every task
Before answering anything about a topic the file covers (prices, names, rules, plans, who does what), read `DECISIONS.md` and follow it. If what the user is asking for now goes against a locked decision, say so in one line and ask if they want to change it. Do not quietly follow the old one or the new one.

## Rules
- IDs are permanent. Never reuse or renumber them.
- One decision per entry.
- Dates are real dates, never "today" or "last week".
- A guess or idea is not a decision. Only lock what the user actually decided.
- Never treat "we might" or "maybe" as locked.
- Killed ideas get locked too ("Decision: no free trial"). Never suggest a killed idea again unless the user brings it back.

## To make every new chat read it
Add this line to the project instructions (CLAUDE.md in Claude Code, or the project's custom instructions in the Claude app):

```
Read DECISIONS.md before answering anything it covers. When I say "lock it in", use the lock-it-in skill.
```
