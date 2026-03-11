from pathlib import Path
import re


def clean_time(text):

    match = re.search(r'(\d{1,4}:\d{2})', text)

    if not match:
        return None

    time_str = match.group(1)
    parts = time_str.split(":")

    if len(parts) == 2:

        menit = int(parts[0])
        detik = int(parts[1])

        jam = menit // 60
        sisa_menit = menit % 60

        return f"{jam:02d}:{sisa_menit:02d}:{detik:02d}"

    elif len(parts) == 3:
        return time_str

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

        times = re.findall(r'(\d{1,4}:\d{2})', line)

        if len(times) >= 2:

            start = clean_time(times[0])
            end = clean_time(times[1])

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