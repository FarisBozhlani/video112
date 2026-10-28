# Albanian vertical edit

Output: `albanian-dynamic-edit.mp4` (1080 × 1920, 30 fps).

The edit preserves the uploaded recording's complete speech and adds animated phrase captions, a three-quality opening hook, alternating digital crops, numbered quality cards, a closing recap, restrained original sound accents, and voice compression. Captions use the user's supplied transcript and timestamp anchors; timing within each anchor is estimated rather than forced-aligned. No external music or stock assets are used.

The original upload was `Recording 2026-10-28 205923.mp4`; the pre-existing `albanian-short.mp4` is unchanged. `captions.ass` is editable with an ASS subtitle editor. `edit.py` generates the captions, audio cues, and FFmpeg filter graph; its workspace paths must be adjusted when reproducing elsewhere. Render with FFmpeg using the original recording as input 0 and `cues.wav` as input 1, the filter graph in `filter.txt`, mappings `[v]` and `[outa]`, H.264 CRF 22, AAC 160 kbps, and `-movflags +faststart`.
