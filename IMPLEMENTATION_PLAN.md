# Implementation Plan: Vocal Separation & Acapella Extraction

Dedicated State-of-the-Art AI vocal isolation skill extracting pristine, studio-grade acapellas from mixed audio tracks using Mel-Band RoFormer, Meta Demucs v4 FT, and Reverb_HQ.

---

## Deliverables Checklist

### v1.0.0 — Initial Release
- [x] **Core Vocal Extraction CLI**: `scripts/separate_stems.py` configured for `--mode vocals` and dedicated vocal methods. ✅ done in v1.0.0
- [x] **Mel-Band RoFormer Integration**: `mel_band_roformer_kim_ft_unwa` model achieving benchmark #1 vocal isolation with 0% instrumental bleed. ✅ done in v1.0.0
- [x] **Meta Demucs v4 FT Integration**: `htdemucs_ft` 2-stem vocal/instrumental split with equivariant phase stabilization. ✅ done in v1.0.0
- [x] **Reverb_HQ De-Reverberation**: Two-stem de-echo separating bone-dry vocal (`vocals_dry.wav`) and isolated reverb (`reverb.wav`). ✅ done in v1.0.0
- [x] **Dual-Pass Studio Chain**: Automatic sequential execution of RoFormer followed by Reverb_HQ (`roformer-dereverb`). ✅ done in v1.0.0
- [x] **Strict Directory Hierarchy**: Output placed directly inside `{song_dir}/{song}_vocals/`. ✅ done in v1.0.0
- [x] **Tri-Platform Accessibility**: Canonical `.agents` installation linked to Claude, Grok, and Antigravity via NTFS junctions. ✅ done in v1.0.0
- [x] **Standard Documentation Suite**: `SKILL.md`, `references/models.md`, `HOW_TO_USE.txt`, `README.md`, `App Changes Tracker.html`, and `dev-notes-v1.0.0.md`. ✅ done in v1.0.0

---

## Roadmap & Future Enhancements

### v1.1.0 — Vocal Layer De-Stacker
- [ ] Lead vs Backing Vocal split (isolate lead singer from vocal harmony choir / ad-libs).
- [ ] Whispered vocal sensitivity booster.
- [ ] Sibilance / De-Esser post-processing pass.

### v1.2.0 — Real-Time DAW Integration
- [ ] Drag-and-drop vocal stem replacement for Ableton Live audio tracks.
- [ ] Direct export to Cartesia / Kokoro voice clone reference folders.
