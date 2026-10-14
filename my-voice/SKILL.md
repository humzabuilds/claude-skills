---
name: my-voice
description: 'Write emails, texts and posts that sound like the user, learned from their real sent messages, and check every claim before showing the draft. Use whenever the user asks Claude to write, draft, reply to or rewrite something they will send as themselves.'
---

# my-voice: sounds like you, and nothing in it is wrong

AI can copy how you sound and still put a wrong fact in your mouth. A robotic sentence gets rewritten. A wrong fact gets believed. This skill does both jobs: it sounds like you, and it only says things that are true.

## Setup (once)
Ask the user to paste 10 to 20 messages they actually sent: emails, texts, DMs. Real ones, not their best writing. Tell them to remove anything private first (phone numbers, addresses, account numbers, other people's details). Save them so every chat can use them:
- Claude Code: a file called `my-voice-samples.md` in the project.
- Claude app: tell the user to add `my-voice-samples.md` to the Project's files, or paste the samples again in a new chat.
If samples already exist, use them and skip this.

From the samples, write down a short profile at the top of the file:
- typical length (count the words in each sample and take the middle one)
- how they open (first few words of each sample)
- how they sign off, or if they do not
- punctuation habits (dashes, exclamation marks, emojis, lowercase)
- words they use a lot, and words they never use

## Every time you draft

### 1. List the facts first
Before writing a word, list every factual claim the message will make: dates, numbers, prices, names, "it's done", "we support", "I sent it". Mark each one:
- **CHECKED:** you can point to where it came from (a file, the thread, something the user just told you).
- **NOT CHECKED:** anything else.

Anything you cannot back up gets cut. If the message needs it, turn it into a question instead. Never soften it into vague wording and leave it in.

Watch for these:
- **A quote you only saw in notes, not in the original source.** Cut it or find the source.
- **A number that appears in only one place.** Ask the user or leave it out.
- **"It works" when you only know it exists.** Say what you actually know.
- **"Yesterday", "Tuesday", "last week".** Check against today's date, or just leave the day out.

### 2. Match their real messages
Pick the 3 to 5 samples closest to this topic and write from them. Match their length, openings, punctuation and words. Do not clean their voice up into polished prose. The roughness is the voice.

### 3. Reject your own draft if
- it is much longer than their typical message and they did not ask for long
- it opens with "I hope this finds you well", "Just wanted to", "Quick note" (unless they do that)
- it has headers or bullet points in a text or short email
- it uses a word they never use
- it sounds balanced and polite when their samples are blunt
- it apologizes when they would not
- it ends by offering a call when they did not ask for one
- it answers more than was asked
- it admits a mistake nobody has noticed, unless the user wants that

### 4. Hand over the draft
Show the full draft, ready to copy and send. If something in it could not be checked and the user needs to know, say that in one plain sentence above the draft. Nothing else.

### 5. Any edit means the whole draft again
When the user asks for a change, however small, show the complete new draft, not just the changed part.

## Re-check before you hand it over
Read the final draft line by line. Any fact that showed up while writing is NOT CHECKED until you check it.
