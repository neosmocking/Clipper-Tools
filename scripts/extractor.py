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

    # Jika format tidak dikenali
    return None


# Fungsi utama untuk mengekstrak timestamp dan judul dari file sumber
def extract_data(input_file, timestamp_out, judul_out):

    print("\n=== EXTRACT TIMESTAMP + JUDUL ===")

    input_path = Path(input_file)

    # Cek apakah file sumber ada
    if not input_path.exists():
        print("File tidak ditemukan.")
        return

    # Membaca seluruh isi file
    content = input_path.read_text(encoding="utf-8")

    # Mengambil semua baris yang mengandung Timestamp
    timestamp_lines = re.findall(r'\*\s*Timestamp:\s*(.*?)\n', content)

    # Mengambil semua judul / hook yang ada di dalam tanda kutip
    hooks = re.findall(r'\*\s*Saran Hook:\s*"(.*?)"', content)

    processed = []

    # Memproses setiap baris timestamp
    for line in timestamp_lines:

        # Mencari semua format waktu (HH:MM:SS atau MM:SS)
        times = re.findall(r'\d{1,2}:\d{2}:\d{2}|\d{1,3}:\d{2}', line)

        # Minimal harus ada start dan end
        if len(times) >= 2:

            start = normalize_time(times[0])
            end = normalize_time(times[1])

            if start and end:
                processed.append(f"{start} - {end}")

    # Membuat folder output jika belum ada
    Path(timestamp_out).parent.mkdir(parents=True, exist_ok=True)

    # Menyimpan hasil timestamp ke file
    with open(timestamp_out, "w", encoding="utf-8") as f:
        for ts in processed:
            f.write(ts + "\n")

    # Membuat folder output untuk judul jika belum ada
    Path(judul_out).parent.mkdir(parents=True, exist_ok=True)

    # Menyimpan semua judul / hook
    with open(judul_out, "w", encoding="utf-8") as f:
        for hook in hooks:
            f.write(hook + "\n")

    # Informasi jumlah data yang berhasil diambil
    print(f"{len(processed)} timestamp ditemukan.")
    print(f"{len(hooks)} judul ditemukan.")
    print("Extract selesai.\n")


def main():

    # Meminta user memasukkan path file sumber    
    raw_path = input("Masukkan path file sumber: ")

    # bersihin + normalize
    sumber_path = os.path.normpath(clean_path(raw_path))
    
    # Lokasi output hasil ekstraksi
    timestamp_file = "data/timestamp.txt"
    judul_file = "data/judul.txt"

    # Menjalankan proses ekstraksi
    extract_data(sumber_path, timestamp_file, judul_file)


# Menjalankan program jika file dieksekusi langsung
if __name__ == "__main__":
    main()