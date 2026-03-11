import re
from pathlib import Path


def clean_filename(text):

    # hapus karakter ilegal windows
    text = re.sub(r'[\\/:*?"<>|]', '', text)

    # ganti spasi dengan underscore
    text = re.sub(r'\s+', '_', text)

    # batasi panjang nama
    return text[:120]


def rename_clips(judul_file, clips_folder):

    judul_path = Path(judul_file)
    clips_path = Path(clips_folder)

    if not judul_path.exists():
        print("judul.txt tidak ditemukan.")
        return

    if not clips_path.exists():
        print("folder clips tidak ditemukan.")
        return

    titles = judul_path.read_text(encoding="utf-8").splitlines()

    # jika baris pertama URL youtube → skip
    if titles and titles[0].startswith("http"):
        titles = titles[1:]

    clips = sorted(clips_path.glob("clip_*.mp4"))

    print(f"\nJumlah clip ditemukan: {len(clips)}")
    print(f"Jumlah judul ditemukan: {len(titles)}\n")

    for i, clip in enumerate(clips):

        if i >= len(titles):
            print(f"Tidak ada judul untuk {clip.name}")
            continue

        title = clean_filename(titles[i])

        new_name = f"{title}.mp4"
        new_path = clips_path / new_name

        try:
            clip.rename(new_path)
            print(f"{clip.name} -> {new_name}")
        except Exception as e:
            print(f"Gagal rename {clip.name}: {e}")

    print("\nRename selesai.\n")


def main():

    print("\n=== RENAME VIDEO ===")

    judul_file = "data/judul.txt"
    clips_folder = "output/clips"

    rename_clips(judul_file, clips_folder)


if __name__ == "__main__":
    main()