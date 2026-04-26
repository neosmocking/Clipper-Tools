from pathlib import Path
import re
import os


def clean_path(p):
    if not p:
        return p
    p = p.strip().strip('"').strip("'")
    return p


# Mengubah berbagai format waktu menjadi format standar HH:MM:SS
def normalize_time(t):

    parts = t.split(":")

    # Jika format sudah HH:MM:SS
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])
        return f"{h:02d}:{m:02d}:{s:02d}"

    # Jika format MM:SS maka dikonversi menjadi HH:MM:SS
    if len(parts) == 2:
        m = int(parts[0])
        s = int(parts[1])

        h = m // 60
        m = m % 60

        return f"{h:02d}:{m:02d}:{s:02d}"

    return None


# Fungsi utama untuk mengekstrak data
def extract_data(input_file, timestamp_out, judul_out, super_title_out):

    print("\n=== EXTRACT TIMESTAMP + JUDUL + SUPER TITLE ===")

    input_path = Path(input_file)

    if not input_path.exists():
        print("File tidak ditemukan.")
        return

    content = input_path.read_text(encoding="utf-8")

    # Timestamp
    timestamp_lines = re.findall(r'\*\s*Timestamp:\s*(.*?)\n', content)

    # Hook (untuk deskripsi)
    hooks = re.findall(r'\*\s*Hook:\s*"(.*?)"', content)

    # Super Title (judul utama dari ###)    
    super_titles = re.findall(r'###\s*(?:\d+\s*[\.:,-]\s*)?(.*)', content)

    processed = []

    # Proses timestamp
    for line in timestamp_lines:

        times = re.findall(r'\d{1,2}:\d{2}:\d{2}|\d{1,3}:\d{2}', line)

        if len(times) >= 2:
            start = normalize_time(times[0])
            end = normalize_time(times[1])

            if start and end:
                processed.append(f"{start} - {end}")

    # Simpan timestamp
    Path(timestamp_out).parent.mkdir(parents=True, exist_ok=True)

    with open(timestamp_out, "w", encoding="utf-8") as f:
        for ts in processed:
            f.write(ts + "\n")

    # Simpan hook (deskripsi)
    Path(judul_out).parent.mkdir(parents=True, exist_ok=True)

    with open(judul_out, "w", encoding="utf-8") as f:
        for hook in hooks:
            f.write(hook.strip() + "\n")

    # Simpan Super Title
    Path(super_title_out).parent.mkdir(parents=True, exist_ok=True)

    with open(super_title_out, "w", encoding="utf-8") as f:
        for title in super_titles:
            title = title.strip()
            if title:  # hindari baris kosong
                f.write(title + "\n")

    # Info hasil
    print(f"{len(processed)} timestamp ditemukan.")
    print(f"{len(hooks)} hook ditemukan.")
    print(f"{len(super_titles)} super title ditemukan.")
    print("Extract selesai.\n")


def main():

    raw_path = input("Masukkan path file sumber: ")
    sumber_path = os.path.normpath(clean_path(raw_path))

    timestamp_file = "data/timestamp.txt"
    judul_file = "data/hook.txt"
    super_title_file = "data/Super_Title.txt"

    extract_data(
        sumber_path,
        timestamp_file,
        judul_file,
        super_title_file
    )


if __name__ == "__main__":
    main()