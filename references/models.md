# Multi-Instrument Stem Separation & Vocal Isolation Models Reference

This reference details the deep neural network architectures utilized by the `stem-separation` and `vocal-separation` skills to isolate individual instruments and extract pristine, studio-grade acapellas.

---

## 1. Multi-Instrument Separation: Meta Demucs v4 (`htdemucs_6s`)

### Architecture
`htdemucs_6s` is a Hybrid Transformer Demucs model trained on multi-track studio stems. It processes both the raw time-domain audio waveform (via a convolutional U-Net) and the frequency-domain spectrogram (via a cross-domain self-attention transformer) in parallel.

### Identified Instrument Channels
1. **`drums.wav`**: Kick drum, snare drum, toms, hi-hats, ride/crash cymbals, claps, and electronic percussion.
2. **`bass.wav`**: Electric bass guitar, upright acoustic bass, synth basslines, and 808 sub-frequencies.
3. **`guitar.wav`**: Acoustic guitars, clean electric guitars, and distorted/overdriven lead and rhythm guitars.
4. **`piano.wav`**: Acoustic grand and upright pianos, electric pianos (Rhodes, Wurlitzer), and keyboard voicings.
5. **`vocals.wav`**: Lead vocals, backing vocal stacks, whispered phrases, and ad-libs.
6. **`other.wav`**: Synthesizers, orchestral strings, brass, woodwinds, sound effects, and background ambient soundscapes.

---

## 2. Dedicated Vocal Isolation: Mel-Band RoFormer (`mel_band_roformer_kim_ft_unwa`)

### Architecture
Mel-Band RoFormer incorporates Rotary Position Embeddings (RoPE) across sub-band spectrograms. It is recognized as the current #1 state-of-the-art vocal isolation architecture in the audio engineering and UVR (Ultimate Vocal Remover) communities.

### Key Strengths
- **Unprecedented Separation Purity**: Achieves an exceptional ~12.44 dB SDR (Signal-to-Distortion Ratio) on vocals.
- **Zero Instrumental Bleed**: Backing acoustic/electric guitars, piano chords, and crash cymbals are completely removed without leaking into the vocal channel.
- **Treble & Air Preservation**: Keeps high-frequency harmonics (10 kHz - 22 kHz), natural vocal breath, and dynamic nuances without metallic phaser or watery swirling artifacts.

---

## 3. High-Precision 2-Stem Isolation: Meta Demucs v4 Fine-Tuned (`htdemucs_ft`)

### Architecture
An ensemble of 4 fine-tuned Hybrid Transformer models trained specifically on MusDB-HQ.

### Key Strengths
- **Equivariant Stabilization**: Running with `--shifts 2` applies random time/phase shifts and averages predictions, eliminating phase cancellation artifacts.
- **Fast Execution**: Excellent quality-to-speed ratio, especially when running on multi-core CPUs.

---

## 4. Vocal De-Reverberation: Reverb HQ (`Reverb_HQ_By_FoxJoy.onnx`)

### Architecture
A dedicated MDX-Net architecture trained on synthetic and real acoustic room response pairs to disentangle dry direct vocal sound from wet acoustic reflections.

### Key Strengths
- **Dry/Wet Separation**: Generates `vocals_dry.wav` (upfront, bone-dry vocal) and `reverb.wav` (isolated room reverb and delay tails).
- **DAW Flexibility**: Allows producers to apply their own compression, EQ, and spatial effects without fighting the room sound of the original recording.
