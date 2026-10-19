#!/usr/bin/env python3
"""Word-by-word captions for a vertical talking-head video.

Needs: ffmpeg on PATH, `pip install openai-whisper pillow`.
Usage: python3 caption.py take.mp4 out.mp4 [--y 0.62] [--words 3] [--accent FFE600] [--font path.ttf] [--fix "clod=claude,..."]
Writes out.mp4 (captions burned in, audio at -14 LUFS, 48 kHz) and out.words.json.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

FONTS = ["/System/Library/Fonts/Supplemental/Arial Black.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/Library/Fonts/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "C:/Windows/Fonts/arialbd.ttf"]
STOP = set("a an the and or but to of in on at for is it i you my your we that this so be with as are was".split())


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    st = j["streams"][0]
    w, h = st["width"], st["height"]
    rot = next((int(sd.get("rotation", 0)) for sd in st.get("side_data_list", []) if "rotation" in sd), 0)
    if abs(rot) % 180 == 90:  # phone clips stored sideways with a rotation flag: ffmpeg turns them upright
        w, h = h, w
    has_audio = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                                "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip() != ""
    return w - w % 2, h - h % 2, float(j["format"]["duration"]), has_audio


def words_from(path, fixes):
    import whisper
    model = whisper.load_model("small")
    res = model.transcribe(path, word_timestamps=True, fp16=False)
    words = []
    for seg in res["segments"]:
        for w in seg.get("words", []):
            t = w["word"].strip()
            if not t:
                continue
            key = re.sub(r"[^\w']", "", t.lower())
            if key in fixes:
                t = re.sub(re.escape(key), fixes[key], t, flags=re.I)
            words.append({"text": t, "start": float(w["start"]), "end": float(w["end"])})
    return words


def beats(words, max_words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        end_sentence = w["text"][-1:] in ".?!,"
        if len(cur) >= max_words or end_sentence:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    # fold a lone short beat into the previous one (no orphan words under 0.45 s)
    merged = []
    for b in out:
        if merged and len(b) == 1 and b[0]["end"] - b[0]["start"] < 0.45 and merged[-1][-1]["text"][-1:] not in ".?!" \
                and len(merged[-1]) < max_words:
            merged[-1] += b
        else:
            merged.append(b)
    return merged


def accent_index(beat):
    # the longest non-stopword, numbers first
    best, score = 0, -1
    for i, w in enumerate(beat):
        k = re.sub(r"[^\w]", "", w["text"].lower())
        s = (100 if any(c.isdigit() for c in k) else 0) + (0 if k in STOP else len(k))
        if s > score:
            best, score = i, s
    return best


def render_png(beat, path, W, H, y, font_path, accent):
    from PIL import Image, ImageDraw, ImageFont
    size = int(W * 0.085)
    font = ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default(size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    toks = [re.sub(r"[.,!?;:]+$", "", w["text"]) for w in beat]
    ai = accent_index(beat)
    space = d.textlength(" ", font=font)
    widths = [d.textlength(t, font=font) for t in toks]
    while sum(widths) + space * (len(toks) - 1) > W * 0.9 and size > 20:
        size -= 4
        font = ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default(size)
        space = d.textlength(" ", font=font); widths = [d.textlength(t, font=font) for t in toks]
    x = (W - (sum(widths) + space * (len(toks) - 1))) / 2
    cy = int(H * y)
    stroke = max(4, size // 12)
    for i, t in enumerate(toks):
        fill = "#" + accent if i == ai else "#FFFFFF"
        d.text((x + 4, cy + 6), t, font=font, fill=(0, 0, 0, 140), anchor="lm")
        d.text((x, cy), t, font=font, fill=fill, stroke_width=stroke, stroke_fill="#000000", anchor="lm")
        x += widths[i] + space
    img.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("take"); ap.add_argument("out")
    ap.add_argument("--y", type=float, default=0.62, help="caption centre as a fraction of height; keep it below the mouth")
    ap.add_argument("--words", type=int, default=3)
    ap.add_argument("--accent", default="FFE600")
    ap.add_argument("--font")
    ap.add_argument("--fix", default="", help='single-word transcription fixes, e.g. "clod=claude,anthropics=anthropic"')
    a = ap.parse_args()
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found: install ffmpeg first")
    a.accent = a.accent.lstrip("#")
    font = a.font or next((f for f in FONTS if os.path.exists(f)), None)
    fixes = dict(kv.split("=", 1) for kv in a.fix.split(",") if "=" in kv)
    W, H, dur, has_audio = probe(a.take)
    if not has_audio:
        sys.exit("this video has no sound track, so there is nothing to caption")
    if W > H:
        print("warning: this video is landscape; captions are laid out for vertical 9:16 video, check --y")
    words = words_from(a.take, {k.lower(): v for k, v in fixes.items()})
    if not words:
        sys.exit("no speech found")
    bs = beats(words, a.words)
    tmp = tempfile.mkdtemp(prefix="cap-")
    try:
        build(a, W, H, dur, font, bs, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"done: {a.out}  ({len(bs)} caption beats, {len(words)} words)")


def build(a, W, H, dur, font, bs, tmp):
    from PIL import Image
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(os.path.join(tmp, "blank.png"))
    lines, t = [], 0.0
    for i, b in enumerate(bs):
        start = b[0]["start"]
        end = bs[i + 1][0]["start"] if i + 1 < len(bs) else min(dur, b[-1]["end"] + 0.4)
        if start > t:
            lines += ["file 'blank.png'", f"duration {start - t:.3f}"]
        p = f"b{i:04d}.png"
        render_png(b, os.path.join(tmp, p), W, H, a.y, font, a.accent)
        lines += [f"file '{p}'", f"duration {max(0.04, end - start):.3f}"]
        t = end
    lines += ["file 'blank.png'", f"duration {max(0.04, dur - t):.3f}", "file 'blank.png'"]
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lines) + "\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.take, "-f", "concat", "-safe", "0", "-i",
                    os.path.join(tmp, "list.txt"), "-filter_complex",
                    "[1:v]format=rgba[c];[0:v]scale=trunc(iw/2)*2:trunc(ih/2)*2[b];[b][c]overlay=0:0:shortest=0:eof_action=pass,format=yuv420p[v];"
                    "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{dur:.3f}", a.out],
                   check=True)
    json.dump([[w for w in b] for b in bs], open(os.path.splitext(a.out)[0] + ".words.json", "w"), indent=1)


if __name__ == "__main__":
    main()
