import subprocess
from pathlib import Path


# Membaca file timestamp.txt lalu mengubahnya menjadi list pasangan waktu
# Contoh isi file:
# 00:01:10 - 00:01:30
# 00:02:00 - 00:02:20
def read_timestamps(file_path):
    timestamps = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Lewati baris kosong
            if not line:
                continue

            # Pisahkan waktu start dan end
            start, end = line.split("-")

            timestamps.append((start.strip(), end.strip()))

    return timestamps


# Fungsi utama untuk memotong video berdasarkan timestamp
def cut_video(input_video, timestamp_file, output_folder):

    video_path = Path(input_video)
    ts_path = Path(timestamp_file)
    out_dir = Path(output_folder)

    # Cek apakah file video ada
    if not video_path.exists():
        print("Video tidak ditemukan.")
        return

    # Cek apakah file timestamp ada
    if not ts_path.exists():
        print("File timestamp tidak ditemukan.")
        return

    # Membuat folder output jika belum ada
    out_dir.mkdir(parents=True, exist_ok=True)

    # Membaca semua timestamp
    timestamps = read_timestamps(ts_path)

    print(f"\nJumlah clip: {len(timestamps)}\n")

    # Loop setiap timestamp untuk membuat clip
    for i, (start, end) in enumerate(timestamps, start=1):

        # Nama file output
        output_file = out_dir / f"clip_{i}.mp4"

        # Perintah ffmpeg untuk memotong video
        cmd = [
            "ffmpeg",
            "-y",  # overwrite file jika sudah ada

            # mulai potong dari waktu ini
            "-ss", start,

            # berhenti di waktu ini
            "-to", end,
            "-i", str(video_path),

            # encode ulang video supaya tidak freeze di awal
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",

            # encode audio
            "-c:a", "aac",
            "-b:a", "192k",

            # memastikan timestamp video dimulai dari 0
            "-avoid_negative_ts", "make_zero",

            str(output_file)
        ]

        print(f"Memotong clip {i}: {start} -> {end}")

        # Menjalankan perintah ffmpeg
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\nSemua clip selesai dibuat.")


def main():

    # Meminta user memasukkan path video sumber
    input_video = input("Masukkan path video sumber: ").strip()

    # Lokasi file timestamp hasil extractor
    timestamp_file = "data/timestamp.txt"

    # Folder output hasil clip
    output_folder = "output/clips"

    # Menjalankan proses pemotongan
    cut_video(input_video, timestamp_file, output_folder)


# Menjalankan program jika file dieksekusi langsung
if __name__ == "__main__":
    main()