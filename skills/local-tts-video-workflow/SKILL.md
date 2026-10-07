---
name: local-tts-video-workflow
description: Produce local TTS narration and integrate it into a video workflow without silently replacing speaker identity or the requested generation route. Use for CosyVoice-style local voices, multilingual segments, subtitle timing, audio import and final video acceptance. 本地配音与剪辑交付。
---

# Local TTS to verified video

## Bind identity and language

Inventory the authorized local runner, interpreter, model and reference audio read-only. Confirm the exact requested voice. A preset, an old custom voice and the user's clone are different identities even if their filenames look similar.

Record a small voice contract: display name, actual configuration/reference, tested languages, consent/use limits and any fallback the user approved. Unknown language support is not inferred from another voice.

If a personal clone is only validated for one language, split foreign-language spans, show exact text and position, and request the user's recording or explicit alternative. Do not quietly switch voice or synthesize an unvalidated mixed-language track.

Confirm voice-cloning permission and rights for reference audio. An official example being downloadable does not establish commercial cloning consent.

## Generate locally when requested

Use the actual local runner. A cloud TTS service is a different route and needs explicit agreement if replacing local generation. Inspect selected device and runtime rather than guessing GPU from hardware presence; use `$windows-gpu-runtime-audit` if relevant.

Generate a short test first. Listen for wrong speaker, plosives, clipped starts, pronunciation and abrupt language switches. Then produce the final narration. Measure real duration; a “30-second” filename is not evidence of a 30-second recording.

## Edit and verify

Import the actual audio into the authorized editor and match visual timing to narration. Maintain transcript and timestamped subtitles. After caption edits, ensure both preview and export use the refreshed text.

Balance music under voice; check clipping and unwanted silence. Export the requested frame size, codec and orientation. Open the final file, inspect start/middle/end, caption wrapping, sync, last frame and audio audibility. Export submission is not completion.

Deliver playable audio/video, subtitles when requested, and editable project when part of the task. Do not package reference voice recordings, consent documents, keys or private training data into public examples.

Acceptance example: requested local male narration remains that verified voice throughout; unsupported foreign spans are explicitly handled; final MP4 and SRT match the approved script and actual audio.
