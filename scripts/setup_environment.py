#!/usr/bin/env python3
"""
Environment Setup & Diagnostics for 'stem-separation' Skill.
Checks and installs state-of-the-art stem separation engines:
- demucs (Meta AI v4 Hybrid Transformer for 4-stem and 6-stem separation)
- audio-separator (Mel-Band RoFormer / BS-RoFormer / MDX-Net for pristine vocal/instrumental separation)
"""

import sys
import subprocess
import importlib.util
import shutil
import argparse
import platform

def check_package(pkg_name):
    return importlib.util.find_spec(pkg_name) is not None

def get_diagnostics():
    info = {}
    info["python"] = sys.version.split()[0]
    info["os"] = f"{platform.system()} {platform.release()}"
    info["ffmpeg_cli"] = shutil.which("ffmpeg") is not None
    info["torch"] = check_package("torch")
    info["cuda_available"] = False
    
    if info["torch"]:
        try:
            import torch
            info["torch_version"] = torch.__version__
            info["cuda_available"] = torch.cuda.is_available()
            if info["cuda_available"]:
                info["cuda_device"] = torch.cuda.get_device_name(0)
        except Exception as e:
            info["torch_error"] = str(e)

    info["demucs"] = check_package("demucs")
    info["audio_separator"] = check_package("audio_separator")
    info["onnxruntime"] = check_package("onnxruntime")
    info["soundfile"] = check_package("soundfile")
    info["av"] = check_package("av")

    return info

def print_diagnostics(info):
    print("=" * 60)
    print("STEM SEPARATION ENVIRONMENT DIAGNOSTICS")
    print("=" * 60)
    print(f"Python Version        : {info['python']}")
    print(f"Operating System      : {info['os']}")
    print(f"System FFmpeg CLI     : {'[OK] Installed' if info['ffmpeg_cli'] else '[!] Not found in PATH (PyAV/SoundFile used)'}")
    print(f"PyAV (built-in codec) : {'[OK] Available' if info.get('av') else '[X] Missing'}")
    print(f"SoundFile             : {'[OK] Available' if info.get('soundfile') else '[X] Missing'}")
    print(f"ONNX Runtime          : {'[OK] Available' if info.get('onnxruntime') else '[X] Missing'}")
    print(f"PyTorch               : {'[OK] Available (' + info.get('torch_version', '') + ')' if info.get('torch') else '[X] Missing'}")
    print(f"CUDA Acceleration     : {'[OK] ' + info.get('cuda_device', 'Yes') if info.get('cuda_available') else '[-] CPU Mode'}")
    print(f"Demucs (Meta v4)      : {'[OK] Installed' if info.get('demucs') else '[X] Not installed'}")
    print(f"Audio-Separator (SOTA): {'[OK] Installed' if info.get('audio_separator') else '[X] Not installed'}")
    print("=" * 60)

    ready = info.get("demucs") or info.get("audio_separator")
    if ready:
        print("[READY] Stem separation engine is ready for processing!")
    else:
        print("[SETUP REQUIRED] To run stem separation, install one of the separation engines:")
        print("  Option A (Recommended for 4-stem & 6-stem):")
        print(f"    {sys.executable} -m pip install -U demucs soundfile")
        print("  Option B (Recommended for cleanest 2-stem RoFormer acapella/instrumental):")
        print(f"    {sys.executable} -m pip install -U \"audio-separator[cpu]\" soundfile")
    print("=" * 60)

def install_packages(engine="all"):
    pkgs = ["soundfile"]
    if engine in ("demucs", "all"):
        pkgs.extend(["demucs", "torch", "torchaudio"])
    if engine in ("audio-separator", "all"):
        pkgs.append("audio-separator[cpu]")

    cmd = [sys.executable, "-m", "pip", "install", "-U"] + pkgs
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Stem separation environment checker and installer.")
    parser.add_argument("--check", action="store_true", help="Print diagnostics")
    parser.add_argument("--install", choices=["demucs", "audio-separator", "all"], default=None, help="Install dependencies")
    args = parser.parse_args()

    if args.install:
        success = install_packages(args.install)
        if success:
            print("\nInstallation finished successfully!")
        else:
            print("\nInstallation encountered errors.", file=sys.stderr)
            sys.exit(1)

    info = get_diagnostics()
    print_diagnostics(info)

if __name__ == "__main__":
    main()
