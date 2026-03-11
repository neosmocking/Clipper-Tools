import subprocess


def run_extractor():
    subprocess.run(["python", "scripts/extractor.py"])


def run_video_cut():
    subprocess.run(["python", "scripts/video_cut.py"])


def run_rename():
    subprocess.run(["python", "scripts/rename_video.py"])


def run_subtitle():
    subprocess.run(["python", "scripts/subtitle_generator.py"])


def main():

    while True:

        print("\n===============================")
        print(" CLIPPER TOOLKIT")
        print("===============================")
        print("1. Extract Timestamp + Judul")
        print("2. Potong Video")
        print("3. Rename Video")
        print("4. Generate Subtitle")
        print("5. Exit")

        choice = input("\nPilih menu: ").strip()

        if choice == "1":
            run_extractor()

        elif choice == "2":
            run_video_cut()

        elif choice == "3":
            run_rename()

        elif choice == "4":
            run_subtitle()

        elif choice == "5":
            print("Keluar dari program.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()