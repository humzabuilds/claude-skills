---
name: video-editor
description: 'Edit a talking-head video into a vertical short (Reels, TikTok, Shorts). First it scores the first 3 seconds on 8 checks and refuses to edit if the hook is weak. If the hook passes, it adds word-by-word captions timed to every spoken word, with one highlighted word per beat, and evens out the audio. Use when the user asks to edit, caption or check a short video, or asks if their hook is good.'
---

# video-editor: no weak hooks, captions on every word

Most bad short videos are not edited badly. They start badly. So this skill grades the opening before it touches anything, and only edits a video that has earned it.

## 1. Get the video and the script
- The video file (vertical, 9:16, one person talking). If there is no file yet, the user can still get step 2 on their script.
- What they say in the first 3 seconds, and what text will be on screen at the start.
- If there is a video, look at it before scoring. Pull 4 frames and open them:
  `ffmpeg -ss 0 -i take.mp4 -vf "fps=1" -frames:v 4 first3_%d.png`
  And hear the opening: `whisper take.mp4 --model small --clip_timestamps 0,4 --output_format txt` (or transcribe the clip and read the first sentence).
  Checks 4, 5 and 6 are about what is on screen, so never score them from a description alone.

## 2. Score the first 3 seconds (the gate)
Score each check 0, 1 or 2. Maximum 16.

| # | Check | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | Reason to keep watching | None | Vague | The viewer can't guess the payoff, or there's a clear finish line ("3 things") |
| 2 | Specific | Generic | One concrete thing | Two or more: a number, a tool, a name, a time |
| 3 | Stakes | Nothing to gain or lose | Mild | Clear gain or loss for this viewer |
| 4 | First frame | Just a face, nothing on screen | Some text or motion | Something real on screen, readable on a phone in under a second |
| 5 | Words, text and picture agree | They disagree or one is missing | Two agree | What is said, the on-screen text and the picture all make the same promise |
| 6 | Proof by second 3 | Only promised | Hinted | The first item or the proof is on screen by second 3 |
| 7 | Who it's for | Nobody | Implied | A clear role or situation |
| 8 | Honest | A made-up claim or hype word | Borderline | Every claim is true and can be shown |

**Pass: 13 or more, and no 0 on checks 1, 4, 5, 6 or 8.**

Also run the mute test: with the sound off, does the first frame's text state the promise on its own?

If it fails, say no. Show the score, the weakest checks, and two rewritten opening lines that would pass. Tell the user to re-record the first 3 seconds. Never put captions or effects on a weak hook to hide it.

## 3. Edit (only after a pass)
Needs `ffmpeg` and Python with `pip install openai-whisper pillow`. In Claude Code, run:

```
python3 <this skill's folder>/scripts/caption.py take.mp4 edited.mp4 --y 0.62
```

It writes down every word with the time it was said, groups them into short beats of 1 to 3 words, highlights one word per beat in yellow, burns the captions in at that moment, and evens the audio out to a steady level (about -14 LUFS, the level the apps play at). The first run downloads the transcription model (about 460 MB) once.

Options:
- `--y 0.62`: how far down the captions sit (0 is the top, 1 the bottom). Keep them below the mouth: around 0.62 to 0.70 for a face filling the frame.
- `--words 3`: most words per beat.
- `--fix "clod=claude"`: fix single words the transcription gets wrong.
- `--accent FFE600`: the highlight colour.

If Python or ffmpeg isn't available (for example in the Claude app), don't pretend to render. Give the user the caption beats with their times and say to run the script in Claude Code.

## 4. Check before handing it over
- Grab 6 frames across the video and look at them: captions never cover the mouth, every beat is readable at phone size, no single word stuck alone on screen.
- Open `edited.words.json` and read every beat against the audio. Fix wrong words with `--fix` and run it again.
- Something should change on screen every 2 to 3 seconds. If the video is one long static shot, tell the user where to cut in a screen recording or a close-up.

## 5. Hand it over
The edited file, the hook score, and anything still worth fixing. Never claim a video will go viral; the score is a checklist, not a promise.
