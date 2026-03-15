from pathlib import Path
import re


def normalize_time(t):

    parts = t.split(":")

    # jika format HH:MM:SS
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])
        return f"{h:02d}:{m:02d}:{s:02d}"

    # jika format MM:SS
    if len(parts) == 2:
        m = int(parts[0])
        s = int(parts[1])

        h = m // 60
        m = m % 60

        return f"{h:02d}:{m:02d}:{s:02d}"

    return None


def extract_data(input_file, timestamp_out, judul_out):

    print("\n=== EXTRACT TIMESTAMP + JUDUL ===")

    input_path = Path(input_file)

    if not input_path.exists():
        print("File tidak ditemukan.")
        return

    content = input_path.read_text(encoding="utf-8")

    timestamp_lines = re.findall(r'\*\s*Timestamp:\s*(.*?)\n', content)
    hooks = re.findall(r'\*\sSaran Hook:\s*"(.*?)"', content)

    processed = []

    for line in timestamp_lines:

        times = re.findall(r'\d{1,2}:\d{2}:\d{2}|\d{1,3}:\d{2}', line)

        if len(times) >= 2:

            start = normalize_time(times[0])
            end = normalize_time(times[1])

            if start and end:
                processed.append(f"{start} - {end}")

    Path(timestamp_out).parent.mkdir(parents=True, exist_ok=True)

    with open(timestamp_out, "w", encoding="utf-8") as f:
        for ts in processed:
            f.write(ts + "\n")

    Path(judul_out).parent.mkdir(parents=True, exist_ok=True)

    with open(judul_out, "w", encoding="utf-8") as f:
        for hook in hooks:
            f.write(hook + "\n")

    print(f"{len(processed)} timestamp ditemukan.")
    print(f"{len(hooks)} judul ditemukan.")
    print("Extract selesai.\n")


def main():

    sumber_path = input("Masukkan path file sumber: ").strip()

    timestamp_file = "data/timestamp.txt"
    judul_file = "data/judul.txt"

    extract_data(sumber_path, timestamp_file, judul_file)


if __name__ == "__main__":
    main()