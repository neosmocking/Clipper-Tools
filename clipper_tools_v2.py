import os
import sys
import subprocess

def clear_screen():
    """Clear terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_venv():
    """Optional warning if user is not running inside a virtual environment."""
    if sys.prefix == sys.base_prefix:
        print("⚠️  [PERINGATAN] Kamu tidak menjalankan script ini di dalam Virtual Environment (venv).")
        print("    Jika terjadi Error 'ModuleNotFoundError', pastikan venv sudah diaktifkan.\n")

def run_script(script_path, *args):
    """
    Menjalankan script Python menggunakan Python Interpreter yang sedang aktif (sys.executable).
    Ini mencegah bentrokan PATH Python sistem di Windows.
    """
    cmd = [sys.executable, script_path] + list(args)
    try:
        return subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Terjadi kesalahan saat menjalankan: {script_path}")
        print(f"Error Code: {e.returncode}")
    except Exception as e:
        print(f"\n❌ Gagal mengeksekusi perintah: {e}")

def main_menu():
    check_venv()
    
    # Path ke direktori scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(base_dir, "scripts")

    extractor_script = os.path.join(scripts_dir, "extractor.py")
    rename_script = os.path.join(scripts_dir, "rename_video.py")
    video_cut_script = os.path.join(scripts_dir, "video_cut.py")
    subtitle_script = os.path.join(scripts_dir, "subtitle_generator.py")

    while True:
        print("==========================================")
        print("           CLIPPER TOOLS MENU             ")
        print("==========================================")
        print("1. Extractor (Audio/Feature Extraction)")
        print("2. Rename Video Files")
        print("3. Video Cut (Pemotong Video)")
        print("4. Subtitle Generator (Whisper)")
        print("5. Jalankan Semua Pipeline (Auto-Process)")
        print("0. Keluar")
        print("==========================================")
        
        choice = input("Pilih menu (0-5): ").strip()

        if choice == '1':
            print("\n--- Menjalankan Extractor ---")
            run_script(extractor_script)
        elif choice == '2':
            print("\n--- Menjalankan Rename Video ---")
            run_script(rename_script)
        elif choice == '3':
            print("\n--- Menjalankan Video Cut ---")
            run_script(video_cut_script)
        elif choice == '4':
            print("\n--- Menjalankan Subtitle Generator ---")
            run_script(subtitle_script)
        elif choice == '5':
            print("\n--- Menjalankan Seluruh Pipeline ---")
            print("[1/3] Memproses Ekstraksi...")
            run_script(extractor_script)
            print("\n[2/3] Memotong Video...")
            run_script(video_cut_script)
            print("\n[3/3] Membuat Subtitle (Whisper)...")
            run_script(subtitle_script)
            print("\n✅ Seluruh proses pipeline selesai!")
        elif choice == '0':
            print("\nTerima kasih telah menggunakan Clipper Tools!")
            sys.exit(0)
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.\n")
        
        input("\nTekan Enter untuk kembali ke menu utama...")
        clear_screen()

if __name__ == "__main__":
    main_menu()