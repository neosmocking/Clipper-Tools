import subprocess
import re
from pathlib import Path


def time_to_seconds(t):

    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s


def get_video_duration(video_path):

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    try:
        return float(result.stdout.strip())
    except:
        return 0


def cut_video(video_path, timestamp_file, output_folder):

    video_path = Path(video_path)
    timestamp_path = Path(timestamp_file)
    output_folder = Path(output_folder)

    if not video_path.exists():
        print("Video tidak ditemukan.")
        return

    if not timestamp_path.exists():
        print("timestamp.txt tidak ditemukan.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    duration = get_video_duration(video_path)

    print(f"\nDurasi video: {round(duration,2)} detik\n")

    timestamps = timestamp_path.read_text().splitlines()

    clip_number = 1

    for line in timestamps:

        match = re.match(r'(\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2})', line)

        if not match:
            print(f"Format timestamp salah -> {line}")
            continue

        start = match.group(1)
        end = match.group(2)

        start_sec = time_to_seconds(start)
        end_sec = time_to_seconds(end)

        if start_sec >= duration or end_sec > duration:

            print(f"Skip: {line} (time stamp tidak ada dalam video)")
            continue

        output_file = output_folder / f"clip_{clip_number}.mp4"

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(video_path),
            "-ss", start,
            "-to", end,
            "-c", "copy",
            str(output_file)
        ]

        print(f"Memotong: {line}")

        subprocess.run(cmd)

        clip_number += 1

    print("\nProses potong video selesai.\n")


def main():

    print("\n=== POTONG VIDEO ===")

    video_path = input("Masukkan path video: ").strip().strip('"')

    timestamp_file = "data/timestamp.txt"
    output_folder = "output/clips"

    cut_video(video_path, timestamp_file, output_folder)


if __name__ == "__main__":
    main()