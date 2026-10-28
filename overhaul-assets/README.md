# Short-form overhaul

A new 45.65-second cut from the original uploaded recording. Earlier exports are preserved.

Source ranges, in seconds: 3–19, 22–27, 34–42, 54–58, 64–76.65. These retain the three qualities and remove repeated explanations. Captions follow the supplied Albanian transcript; within-anchor phrase timing is estimated.

New visual treatment: charcoal framing, large white/yellow kinetic phrase captions, emerald vector illustrations, numbered chapter headers, 2.8-second alternating digital crops, opening push-in, advancing progress track, and closing three-quality recap. The original quiet speech is amplified and normalized toward -16 LUFS with peak limiting. Original synthesized transition cues sit under the voice; no background music is used.

Editable captions, transcript, generator, filter graph, and cues are included. To reproduce elsewhere, adjust the /workspace/video-overhaul paths in build.py and filter.txt. Use the original uploaded recording as FFmpeg input 0 and cues.wav as input 1; apply filter.txt, map [v] and [outa], encode H.264 CRF 21 / AAC 192k with faststart. The generator requires Python's standard library only. FFmpeg requires libass and libx264.
