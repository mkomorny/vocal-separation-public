---
name: vocal-separation
description: Dedicated State-of-the-Art AI vocal separation and acapella extraction (Mel-Band RoFormer, Meta Demucs v4 Fine-Tuned, De-Reverberation, and Multi-Pass Studio chains). Interactively presents vocal separation methods with a recap of their strengths before separating.
---

# Dedicated Vocal Separation & Acapella Extraction

State-of-the-Art vocal isolation skill compatible with **Claude (Chat, Code, Cowork)**, **Grok CLI**, and **Antigravity**.

Designed specifically for isolating pristine, studio-grade acapellas from mixed audio tracks, eliminating background instrumental bleed, and stripping room reflections/reverb.

---

## Core Principles & Guarantees

### 1. Mandatory Pre-Separation Selection
Whenever the user requests vocal separation, acapella extraction, or runs `/vocal-separation`, the agent **MUST ALWAYS ask the user which vocal separation method they prefer**, providing a concise recap of each option's unique strengths before executing.

### 2. Available Vocal Separation Methods & Strengths

| Option | Method Code | Architecture / Engine | Strengths & Best Use Cases |
| :--- | :--- | :--- | :--- |
| **1. Mel-Band RoFormer** *(Recommended)* | `roformer` | **Mel-Band RoFormer (`mel_band_roformer_kim_ft_unwa`)** | **Maximum Purity & Zero Bleed**: Ranked #1 vocal isolation architecture in the world (UVR benchmark leader). Eliminates 100% of backing instruments (even heavy guitars, cymbals, synth walls). Preserves natural vocal breath and pristine upper treble (>10 kHz) without watery phase artifacts. |
| **2. Demucs Fine-Tuned 2-Stem** | `demucs-ft` | **Meta Demucs v4 FT (`htdemucs_ft`, shifts=2, overlap=0.5)** | **Fast & Reliable**: Low CPU/memory overhead, fast execution. Dedicated 2-stem vocal/instrumental split with equivariant phase stabilization to prevent robotic swirling. Great for quick, balanced acapella isolation. |
| **3. Vocal De-Reverberation** | `de-reverb` | **Reverb HQ (`Reverb_HQ_By_FoxJoy.onnx`)** | **Bone-Dry Vocals**: Strips wet room reflections, hall echo, and delay tails. Outputs upfront `vocals_dry.wav` and isolated `reverb.wav` (ideal for remixing or re-processing in a DAW). |
| **4. RoFormer + De-Reverb Dual Pass** | `roformer-dereverb` | **Mel-Band RoFormer + Reverb HQ** | **Ultimate Studio Acapella**: Two-stage pipeline. Pass 1 strips 100% of instrumental backing with RoFormer; Pass 2 strips room reverb with Reverb_HQ. Yields an ultra-clean, completely dry studio acapella. |
| **5. Standard Baseline** | `standard` | **Meta Demucs v4 (`htdemucs_6s`)** | **Quick Preview**: Fast single-pass baseline extraction matching standard multi-stem split. |

### 3. Strict Folder Location Guarantee
Isolated vocals MUST always be placed into a dedicated subfolder created **inside whichever directory the original audio file resides in**:
```
{original_song_directory}/{original_song_name}_vocals/
├── vocals.wav
├── vocals_dry.wav          # (if de-reverb or dual-pass selected)
├── reverb.wav              # (if de-reverb or dual-pass selected)
├── instrumental.wav        # (if 2stem mode requested)
└── stems_manifest.json
```
Never dump audio files into temporary folders or the working directory.

---

## Agent Execution Workflow

When the user asks to isolate vocals or runs `/vocal-separation "<AUDIO_PATH>"`:

### Step 1: Identify Audio File
Verify the target audio file path exists (`.wav`, `.mp3`, `.flac`, `.m4a`, etc.).

### Step 2: Prompt the User for Vocal Method
In **Antigravity**, invoke the `ask_question` tool with the options and their recaps.
In **Claude Code / Grok CLI / chat interfaces**, present the numbered options with their recaps in chat:

```text
Which vocal separation method would you like to use?

1. (Recommended) Mel-Band RoFormer (`roformer`)
   - Strengths: World #1 SOTA isolation, zero instrumental bleed (heavy guitars/cymbals disappear), crisp air (>10 kHz).
2. Meta Demucs v4 Fine-Tuned 2-Stem (`demucs-ft`)
   - Strengths: Fast execution, lower memory overhead, equivariant phase stabilization eliminates watery artifacts.
3. Vocal De-Reverberation (`de-reverb`)
   - Strengths: Strips room reflections and delay tails into dry vocal (`vocals_dry.wav`) and reverb track (`reverb.wav`).
4. RoFormer + De-Reverb Dual Pass (`roformer-dereverb`)
   - Strengths: Ultimate studio quality. Eliminates all instrumental spill AND strips room ambience for bone-dry acapella.
5. Standard Baseline (`standard`)
   - Strengths: Quick preview matching standard Demucs baseline.
```

### Step 3: Run Separation Script
Execute the bundled separation script with `--mode vocals` and `--vocal-method`:

```bash
python "C:\Users\<you>\.agents\skills\vocal-separation\scripts\separate_stems.py" "<AUDIO_PATH>" --mode vocals --vocal-method <SELECTED_METHOD>
```

Examples:
```bash
# Mel-Band RoFormer (SOTA zero bleed):
python "C:\Users\<you>\.agents\skills\vocal-separation\scripts\separate_stems.py" "C:\Music\Song.mp3" --mode vocals --vocal-method roformer

# Demucs Fine-Tuned 2-Stem:
python "C:\Users\<you>\.agents\skills\vocal-separation\scripts\separate_stems.py" "C:\Music\Song.mp3" --mode vocals --vocal-method demucs-ft

# RoFormer + De-Reverb Dual Pass:
python "C:\Users\<you>\.agents\skills\vocal-separation\scripts\separate_stems.py" "C:\Music\Song.mp3" --mode vocals --vocal-method roformer-dereverb
```

### Step 4: Present Results
List the extracted audio tracks with clickable markdown file links:
- `VOCALS` -> [vocals.wav](file:///...)
- `VOCALS (DRY)` -> [vocals_dry.wav](file:///...) *(if de-reverb)*
- `REVERB TAILS` -> [reverb.wav](file:///...) *(if de-reverb)*
- `MANIFEST` -> [stems_manifest.json](file:///...)
