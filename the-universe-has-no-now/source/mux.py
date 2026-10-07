"""Mux picture + mix into film.mp4 (H.264 / AAC 48 kHz), keeping the deliverable under GitHub's 100 MB limit.
The high-quality master (CRF 18) stays in build/film_master.mp4."""
import os, sys, json, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
video = os.path.join(ROOT, "build", "film_video.mp4"); audio = os.path.join(ROOT, "audio", "mix.wav")
master = os.path.join(ROOT, "build", "film_master.mp4"); out = os.path.join(ROOT, "film.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                "-shortest", "-movflags", "+faststart", master], check=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", master], capture_output=True, text=True).stdout)
size = os.path.getsize(master)
limit = 92 * 1024 * 1024
if size <= limit:
    subprocess.run(["cp", master, out], check=True); print("film.mp4 = master", size // 2 ** 20, "MB")
else:
    # two-pass to a target total bitrate that fits
    vbr = int((limit * 8 / dur - 256e3) / 1000 * 0.97)
    print(f"master {size//2**20} MB > limit; re-encoding video at {vbr} kb/s (two-pass)")
    log = os.path.join(ROOT, "build", "x264pass")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-c:v", "libx264", "-preset", "medium", "-b:v", f"{vbr}k", "-pass", "1", "-passlogfile", log, "-an", "-f", "null", "/dev/null"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", audio, "-c:v", "libx264", "-preset", "medium", "-b:v", f"{vbr}k", "-pass", "2", "-passlogfile", log,
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    print("film.mp4", os.path.getsize(out) // 2 ** 20, "MB")
