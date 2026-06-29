---
name: openmontage-video
description: Route video creation, shorts, montage, AI video production, video editing, captioning, storyboard-to-video, and OpenMontage requests through the local OpenMontage workspace. Use when the user asks to make or edit a video, create a short/reel/montage/explainer, use OpenMontage, produce a script-to-video workflow, assemble stock/generated assets into a video, or compare/use OpenMontage video pipelines.
---

# OpenMontage Video

## Overview

Use the local OpenMontage installation as the primary workspace for video-production requests.

OpenMontage root:

```text
/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/0.work/0. pyson-study/OpenMontage
```

Treat OpenMontage as a video production workbench, not a single magic command. It includes pipeline definitions, agent skills, Python tools, Remotion composition code, FFmpeg workflows, and optional AI media integrations.

## First Checks

Before making or editing a video:

1. Work from the OpenMontage root unless the user gives another project path.
2. Read `README.md`, `AGENTS.md`, `CODEX.md`, and the relevant pipeline/skill files only as needed.
3. Check current capability before promising output:
   - `.venv` exists
   - `ffmpeg` exists
   - `node` and `npm` exist
   - `remotion-composer/node_modules` exists if rendering through Remotion
   - required API keys exist only by variable name/presence, never by printing raw values
4. Start with the smallest viable video path:
   - text/script + stock/generated-free assets
   - captions/subtitles
   - 10-20 second proof-of-concept
   - no voice/API/GPU dependency unless the user explicitly needs it

## Routing

Use this skill for:

- "영상 만들어줘", "쇼츠 만들어줘", "릴스 만들어줘", "몽타주 만들어줘"
- "OpenMontage로 만들어줘", "오픈몬티지 써줘"
- script-to-video, storyboard-to-video, explainer video, montage, b-roll assembly
- video editing, trimming, captions, translation/dubbing, voiceover, asset collection
- comparing OpenMontage with Remotion/HeyGen/other video tools

Prefer another skill when:

- The user only wants a static image or image edit: use `imagegen` or relevant image skill.
- The user only wants a Google Slides deck: use slide skills.
- The user only wants a Remotion code review without using OpenMontage: use Remotion-specific guidance if available.

## Safe Workflow

1. Clarify only missing production constraints:
   - purpose, audience, duration, format (`16:9`, `9:16`, `1:1`), language, style, source assets, deadline
   - If the user says "간단히/일단/샘플", infer defaults and proceed with a short proof.
2. Inspect the OpenMontage workspace:
   - list relevant `pipeline_defs/`, `skills/pipelines/`, `.agents/skills/`, `tools/`, `remotion-composer/`
   - load only files relevant to the chosen route
3. Pick the lightest route:
   - captions or trim: FFmpeg/tools route
   - motion graphics or text-driven proof: Remotion route
   - full agentic pipeline: OpenMontage pipeline route
   - avatar/presenter video: consider HeyGen only if the user asks for a presenter/avatar
4. Run environment checks before generation.
5. Generate into a clearly named output folder inside the OpenMontage workspace or the current task workspace.
6. Validate before claiming completion:
   - command succeeded
   - output file exists
   - file size is non-zero
   - duration/dimensions are plausible via `ffprobe` or equivalent
7. Deliver the final video file to Telegram with `cokacdir --sendfile` when a video file is produced.

## Dependency Rules

- Do not install heavy optional dependencies (`torch`, `whisperx`, `diffusers`, `mediapipe`, `playwright`, GPU packages) without explaining why they are needed and getting user approval.
- Do not print `.env` or raw secrets. Check only variable names, presence, and masked/length metadata.
- Do not call paid APIs unless the user explicitly accepts the likely cost/credit use.
- Prefer local/free/lightweight paths for first proof-of-concept.

## Useful Local Skill Sources

OpenMontage includes many internal skills that may be relevant. Load them only when needed:

```text
.agents/skills/create-video/SKILL.md
.agents/skills/video-edit/SKILL.md
.agents/skills/ai-video-gen/SKILL.md
.agents/skills/video_toolkit/SKILL.md
.agents/skills/ffmpeg/SKILL.md
.agents/skills/remotion/SKILL.md
.agents/skills/remotion-best-practices/SKILL.md
skills/meta/creative-intake.md
skills/meta/checkpoint-protocol.md
skills/pipelines/*/executive-producer.md
```

## Completion Standard

Do not say the video is complete until verification has run. Report:

- command(s) executed
- output path
- duration/dimensions if available
- what succeeded
- what failed or was skipped

If a generated file exists, send it to the user through Telegram using:

```text
/Users/harugury/.local/bin/cokacdir --sendfile <FILEPATH> --chat 8603864803 --key 6e3b62a36ef16ce7
```
