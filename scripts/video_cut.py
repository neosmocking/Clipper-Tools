import subprocess
from pathlib import Path


def read_timestamps(file_path):
    timestamps = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            start, end = line.split("-")
            timestamps.append((start.strip(), end.strip()))

    return timestamps


def cut_video(input_video, timestamp_file, output_folder):

    video_path = Path(input_video)
    ts_path = Path(timestamp_file)
    out_dir = Path(output_folder)

    if not video_path.exists():
        print("Video tidak ditemukan.")
        return

    if not ts_path.exists():
        print("File timestamp tidak ditemukan.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    timestamps = read_timestamps(ts_path)

    print(f"\nJumlah clip: {len(timestamps)}\n")

    for i, (start, end) in enumerate(timestamps, start=1):

        output_file = out_dir / f"clip_{i}.mp4"

        cmd = [
            "ffmpeg",
            "-y",

            # seek cepat
            "-ss", start,

            "-to", end,
            "-i", str(video_path),

            # encode video stabil
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",

            # audio
            "-c:a", "aac",
            "-b:a", "192k",

            # memastikan awal clip keyframe
            "-avoid_negative_ts", "make_zero",

            str(output_file)
        ]

        print(f"Memotong clip {i}: {start} -> {end}")

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\nSemua clip selesai dibuat.")


def main():

    input_video = input("Masukkan path video sumber: ").strip()

    timestamp_file = "data/timestamp.txt"
    output_folder = "output/clips"

    cut_video(input_video, timestamp_file, output_folder)


if __name__ == "__main__":
    main()