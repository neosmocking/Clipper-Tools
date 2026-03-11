# Clipper Toolkit

Toolkit sederhana berbasis Python untuk membantu workflow **video clipping otomatis**: mulai dari ekstraksi timestamp, pemotongan video, rename clip, hingga pembuatan subtitle menggunakan Whisper.

Tool ini dirancang untuk mempercepat proses membuat **short-form content** seperti YouTube Shorts, TikTok, dan Reels dari video panjang.

---

# Features

* Extract timestamp dan judul dari file teks
* Memotong video otomatis berdasarkan timestamp
* Rename clip video berdasarkan judul
* Generate subtitle (.srt) menggunakan Whisper
* Pilihan model Whisper (tiny → large)
* Deteksi GPU otomatis (CUDA jika tersedia)

---

# Project Structure

```
clipper_toolkit/

clipper_tools.py

scripts/
 ├ extractor.py
 ├ video_cut.py
 ├ rename_video.py
 └ subtitle_generator.py

data/
output/
```

Output utama berada di:

```
output/clips/
```

---

# Requirements

* Python 3.9+
* FFmpeg
* GPU opsional (untuk Whisper lebih cepat)

Install dependency Python:

```
pip install -r requirements.txt
```

---

# Install FFmpeg

Tool pemotong video menggunakan **FFmpeg**.

Download:

https://ffmpeg.org/download.html

Setelah install pastikan command ini bekerja di terminal:

```
ffmpeg -version
```

---

# Cara Menjalankan

Masuk ke folder project lalu jalankan:

```
python clipper_tools.py
```

Menu toolkit:

```
===============================
 CLIPPER TOOLKIT
===============================

1. Extract Timestamp + Judul
2. Potong Video
3. Rename Video
4. Generate Subtitle
5. Exit
```

---

# Workflow Penggunaan

Langkah umum:

1️⃣ Extract timestamp dari file teks

```
input → sumber.txt
output → data/timestamp.txt
output → data/judul.txt
```

2️⃣ Potong video berdasarkan timestamp

```
input → video.mp4
output → output/clips/clip_1.mp4
```

3️⃣ Rename clip berdasarkan judul

```
clip_1.mp4 → Judul_video.mp4
```

4️⃣ Generate subtitle otomatis

```
Judul_video.mp4 → Judul_video.srt
```

---

# Whisper Models

Model yang tersedia:

| Model  | Speed         | Akurasi      |
| ------ | ------------- | ------------ |
| tiny   | sangat cepat  | rendah       |
| base   | cepat         | cukup        |
| small  | seimbang      | bagus        |
| medium | lambat        | sangat bagus |
| large  | paling lambat | terbaik      |

Untuk workflow clip biasanya **small** atau **medium** sudah cukup.

---

# Catatan

Jika timestamp melebihi durasi video, script akan **skip otomatis** tanpa menghentikan proses.

---

# License

MIT License
