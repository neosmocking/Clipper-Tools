import os
import whisper
import torch
from datetime import datetime

# -----------------------
# Fungsi Utility
# -----------------------

def format_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(segments, srt_path):
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg['start'])
            end = format_time(seg['end'])
            text = seg['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def transcribe_video(file_path, model, lang):
    print(f"\nTranskrip video: {file_path}")
    result = model.transcribe(file_path, language=lang)
    return result["segments"]


# -----------------------
# Pilihan bahasa
# -----------------------

print("Pilih Bahasa Transkripsi:")
print("1. Indonesia")
print("2. Inggris")

lang_choice = input("Masukkan pilihan (1/2): ").strip()
language = "id" if lang_choice == "1" else "en"


# -----------------------
# Pilihan model Whisper
# -----------------------

print("\nPilih Model Whisper:")
print("1. Tiny")
print("2. Base")
print("3. Small")
print("4. Medium")
print("5. Large")

model_choice = input("Masukkan pilihan (1-5): ").strip()

model_dict = {
    "1": "tiny",
    "2": "base",
    "3": "small",
    "4": "medium",
    "5": "large"
}

model_name = model_dict.get(model_choice, "base")


# -----------------------
# Folder clips
# -----------------------

clips_folder = "output/clips"

video_extensions = [
    ".mp4", ".mkv", ".mov", ".avi",
    ".mp3", ".wav", ".m4a", ".aac", ".flac"
]

files_to_process = []

if not os.path.isdir(clips_folder):
    print("Folder output/clips tidak ditemukan.")
    exit(1)

for f in os.listdir(clips_folder):
    full_path = os.path.join(clips_folder, f)

    if os.path.isfile(full_path) and any(f.lower().endswith(ext) for ext in video_extensions):
        files_to_process.append(full_path)

if not files_to_process:
    print("Tidak ada video di folder clips.")
    exit(1)


# -----------------------
# Device GPU/CPU
# -----------------------

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "float32"

print(f"\nDevice: {device}, compute_type: {compute_type}")


# -----------------------
# Load model Whisper
# -----------------------

print(f"Loading Whisper model '{model_name}'...")
model = whisper.load_model(model_name, device=device)


# -----------------------
# Proses setiap video
# -----------------------

for file_path in files_to_process:

    try:

        base_name = os.path.basename(file_path)
        name_no_ext, _ = os.path.splitext(base_name)

        srt_file = os.path.join(clips_folder, f"{name_no_ext}.srt")

        if os.path.exists(srt_file):
            print(f"{srt_file} sudah ada, skip.")
            continue

        segments = transcribe_video(file_path, model, language)

        write_srt(segments, srt_file)

        print(f"SRT berhasil dibuat: {srt_file}")

    except Exception as e:

        print(f"Error pada file {base_name}: {e}")

        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {base_name}: {e}\n")


print("\nSelesai semua video! Subtitle ada di folder clips.")