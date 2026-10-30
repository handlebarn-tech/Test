"""Project-original 2-note door chime (ding-dong, E5 -> C5), deterministic 16-bit mono 44.1 kHz WAV.

Usage: python -I Tools/Assets/make_chime.py [out.wav]  (default: shared cache original/ORIG-CHIME/door_chime.wav)
"""
import os, sys, wave
import numpy as np

SR = 44100
OUT = "C:/Users/handl/Downloads/Dispo Game Assets Cache/original/ORIG-CHIME/door_chime.wav"


def bell(freq, dur):
    t = np.arange(int(SR * dur)) / SR
    # inharmonic partials + exponential decay give a struck-bar timbre
    tone = sum(a * np.sin(2 * np.pi * freq * m * t) for m, a in [(1, 1.0), (2.76, 0.35), (5.4, 0.12)])
    return tone * np.exp(-t * 3.0) * np.minimum(1, t / 0.004)


def chime():
    a, b = bell(659.25, 1.6), bell(523.25, 2.2)
    out = np.zeros(int(SR * 0.55) + len(b))
    out[:len(a)] += a
    out[int(SR * 0.55):] += b
    return (out / np.abs(out).max() * 0.8 * 32767).astype("<i2")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else OUT
    pcm = chime()
    assert len(pcm) > SR and np.abs(pcm).max() > 20000, "chime silent or truncated"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(path, len(pcm) / SR, "s")
