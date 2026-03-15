import re
from pathlib import Path


# Membersihkan teks agar aman dijadikan nama file
def clean_filename(text):

    # Hapus karakter ilegal di Windows
    text = re.sub(r'[\\/:*?"<>|]', '', text)

    # Rapikan spasi berlebih
    text = re.sub(r'\s+', ' ', text)

    text = text.strip()

    # Ganti spasi menjadi underscore
    text = text.replace(" ", "_")

    # Jika judul kosong gunakan fallback
    if text == "":
        text = "clip"

    # Batasi panjang nama file
    return text[:120]


def rename_clips(judul_file, clips_folder):

    # Path file judul dan folder clip
    judul_path = Path(judul_file)
    clips_path = Path(clips_folder)

    # Baca semua judul dari file
    titles = judul_path.read_text(encoding="utf-8").splitlines()

    # Jika baris pertama berisi URL (kadang dari hasil AI), skip
    if titles and titles[0].startswith("http"):
        titles = titles[1:]

    # Ambil semua file clip
    clips = list(clips_path.glob("clip_*.mp4"))

    # Urutkan clip secara natural (clip_1, clip_2, clip_10)
    clips.sort(key=lambda x: int(x.stem.split("_")[1]))

    # Debug jumlah clip dan judul
    print("\n--- DEBUG ---")
    print("Jumlah clip :", len(clips))
    print("Jumlah judul:", len(titles))
    print("-------------\n")

    # ------------------------
    # Tahap 1: rename sementara
    # ------------------------
    # Menghindari konflik nama saat rename massal
    temp_files = []
    for clip in clips:
        temp_path = clip.with_name(f"temp_{clip.name}")
        clip.rename(temp_path)
        temp_files.append(temp_path)

    # Menyimpan nama file yang sudah digunakan
    used_names = set()

    # ------------------------
    # Tahap 2: rename final
    # ------------------------
    for i, clip in enumerate(temp_files):

        # Jika judul tidak cukup, skip
        if i >= len(titles):
            print("Skip:", clip.name)
            continue

        # Bersihkan judul agar aman jadi nama file
        title = clean_filename(titles[i])

        # Tambahkan nomor urut di depan
        number = f"{i+1:02d}"
        new_name = f"{number}_{title}.mp4"

        # Jika nama sudah ada, tambahkan counter
        counter = 2
        while new_name in used_names or (clips_path / new_name).exists():
            new_name = f"{number}_{title}_{counter}.mp4"
            counter += 1

        new_path = clips_path / new_name

        # Rename file
        clip.rename(new_path)
        used_names.add(new_name)

        print(f"{clip.name} -> {new_name}")

    print("\nRename selesai.")


def main():

    # Lokasi file input
    judul_file = "data/judul.txt"
    clips_folder = "output/clips"

    rename_clips(judul_file, clips_folder)


if __name__ == "__main__":
    main()