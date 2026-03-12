import re
from pathlib import Path


# -----------------------
# Bersihkan nama file
# -----------------------
def clean_filename(text):

    # hapus karakter ilegal windows
    text = re.sub(r'[\\/:*?"<>|]', '', text)

    # ganti spasi berlebih
    text = re.sub(r'\s+', ' ', text)

    text = text.strip()

    # ganti spasi dengan underscore
    text = text.replace(" ", "_")

    # batasi panjang nama file
    return text[:120]


# -----------------------
# Rename Clips
# -----------------------
def rename_clips(judul_file, clips_folder):

    judul_path = Path(judul_file)
    clips_path = Path(clips_folder)

    if not judul_path.exists():
        print("File judul.txt tidak ditemukan.")
        return

    if not clips_path.exists():
        print("Folder clips tidak ditemukan.")
        return

    titles = judul_path.read_text(encoding="utf-8").splitlines()

    # skip baris pertama jika URL
    if titles and titles[0].startswith("http"):
        titles = titles[1:]

    # ambil semua clip
    clips = list(clips_path.glob("clip_*.mp4"))

    if not clips:
        print("Tidak ada clip ditemukan.")
        return

    # -----------------------
    # Natural sort clip_1, clip_2, clip_10
    # -----------------------
    clips.sort(key=lambda x: int(x.stem.split("_")[1]))

    print(f"\nJumlah clip ditemukan : {len(clips)}")
    print(f"Jumlah judul ditemukan: {len(titles)}\n")

    used_names = set()

    for i, clip in enumerate(clips):

        if i >= len(titles):
            print(f"Tidak ada judul untuk {clip.name}")
            continue

        title = clean_filename(titles[i])

        new_name = f"{title}.mp4"

        # cegah duplikat nama
        counter = 2
        while new_name in used_names or (clips_path / new_name).exists():
            new_name = f"{title}_{counter}.mp4"
            counter += 1

        new_path = clips_path / new_name

        try:
            clip.rename(new_path)
            used_names.add(new_name)
            print(f"{clip.name} -> {new_name}")

        except Exception as e:
            print(f"Gagal rename {clip.name}: {e}")

    print("\nRename selesai.\n")


# -----------------------
# MAIN
# -----------------------
def main():

    print("\n=== RENAME VIDEO ===")

    judul_file = "data/judul.txt"
    clips_folder = "output/clips"

    rename_clips(judul_file, clips_folder)


if __name__ == "__main__":
    main()