# Dedicated Vocal Separation & Acapella Extraction

> **Tri-Platform Agent Skill** for Claude Desktop / Code, Grok CLI, and Google Antigravity / Gemini.  
> Dedicated State-of-the-Art AI vocal separation and studio acapella extraction using Mel-Band RoFormer, Meta Demucs v4 Fine-Tuned, and Reverb_HQ de-reverberation.

---

## Overview

Separating vocals from modern commercial mixes requires handling dense walls of sound—distorted electric guitars, crashing cymbals, stereo synths, and heavy reverb. 

**`vocal-separation`** is engineered specifically for isolating pristine, studio-grade acapellas from mixed audio tracks, eliminating 100% of instrumental bleed, and stripping room reflections into separate dry and wet tracks.

---

## Vocal Isolation Engines & Benchmark Highlights

| Engine | Method Code | Architecture | Strengths & Best Use Cases |
| :--- | :--- | :--- | :--- |
| **Mel-Band RoFormer** *(Recommended)* | `roformer` | `mel_band_roformer_kim_ft_unwa` | **Ranked #1 in the World**: UVR benchmark leader. Completely removes heavy guitars, cymbals, and synths without watery phase artifacts. Preserves upper treble air (>10 kHz). |
| **Meta Demucs v4 FT** | `demucs-ft` | `htdemucs_ft` (2-Stem) | **Fast & Reliable**: Low CPU/RAM footprint. Equivariant phase stabilization prevents swirling artifacts. Ideal for quick, balanced 2-stem acapella/instrumental splits. |
| **Vocal De-Reverberation** | `de-reverb` | `Reverb_HQ_By_FoxJoy.onnx` | **Bone-Dry Vocals**: Strips room acoustics, hall reflections, and delay tails into dry vocals (`vocals_dry.wav`) and isolated reverb (`reverb.wav`). |
| **RoFormer + De-Reverb Dual Pass** | `roformer-dereverb` | RoFormer + Reverb_HQ | **Ultimate Studio Acapella**: Pass 1 strips 100% of instrumental backing; Pass 2 strips room ambience, delivering a bone-dry, upfront vocal. |

---

## CLI Usage

Run the separation CLI standalone or via agent background tasks:

```bash
# 1. Mel-Band RoFormer (World #1 SOTA zero-bleed acapella):
python scripts/separate_stems.py "C:\Music\Song.mp3" --mode vocals --vocal-method roformer

# 2. Meta Demucs v4 FT (Fast 2-stem vocal/backing split):
python scripts/separate_stems.py "C:\Music\Song.mp3" --mode vocals --vocal-method demucs-ft

# 3. Two-Stage Bone-Dry Studio Acapella (RoFormer + De-Reverb):
python scripts/separate_stems.py "C:\Music\Song.mp3" --mode vocals --vocal-method roformer-dereverb

# 4. Standalone De-Reverberation on an already isolated vocal:
python scripts/separate_stems.py "C:\Music\Acapella.wav" --mode de-reverb
```

### Output Layout
```
{original_song_directory}/{original_song_name}_vocals/
├── vocals.wav
├── vocals_dry.wav          # (if de-reverb or dual-pass selected)
├── reverb.wav              # (if de-reverb or dual-pass selected)
├── instrumental.wav        # (if 2stem mode requested)
└── stems_manifest.json
```

---

## Tri-Platform Architecture

Zero duplicate code across tools. Canonical source resides in `.agents`:
- **Canonical**: `C:\Users\<you>\.agents\skills\vocal-separation`
- **Claude**: `C:\Users\<you>\.claude\skills\vocal-separation` (NTFS Junction)
- **Grok**: `C:\Users\<you>\.grok\skills\vocal-separation` (NTFS Junction)
- **Antigravity**: `C:\Users\<you>\.gemini\config\skills\vocal-separation` (NTFS Junction)

---

## Documentation Suite

- [`HOW_TO_USE.txt`](file:///C:/Users/<you>/.agents/skills/vocal-separation/HOW_TO_USE.txt): Standardized user guide and prompt templates.
- [`IMPLEMENTATION_PLAN.md`](file:///C:/Users/<you>/.agents/skills/vocal-separation/IMPLEMENTATION_PLAN.md): Feature checklist and roadmap.
- [`App Changes Tracker.html`](file:///C:/Users/<you>/.agents/skills/vocal-separation/App%20Changes%20Tracker.html): Interactive visual version log.
- [`SKILL.md`](file:///C:/Users/<you>/.agents/skills/vocal-separation/SKILL.md): Agent system instructions and triggers.
- [`references/models.md`](file:///C:/Users/<you>/.agents/skills/vocal-separation/references/models.md): Technical deep-dive into model architectures and benchmarks.
