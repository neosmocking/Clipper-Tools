# Clipper Toolkit

Toolkit Python sederhana untuk membantu workflow **video clipping otomatis**: mulai dari ekstraksi timestamp dari teks, memotong video, rename clip, hingga membuat subtitle menggunakan Whisper.

Tool ini dirancang untuk mempercepat pembuatan **short-form content** seperti YouTube Shorts, TikTok, dan Reels dari video panjang.

---

# Features

* Extract **timestamp dan judul** dari file teks
* Memotong video otomatis berdasarkan timestamp
* Rename clip video berdasarkan judul
* Generate subtitle `.srt` menggunakan Whisper
* Pilihan model Whisper (tiny → large)
* Deteksi GPU otomatis (CUDA jika tersedia)
* Skip otomatis jika timestamp melebihi durasi video

---

# Workflow

Pipeline kerja toolkit ini:

```
Text Input
   ↓
Extract Timestamp + Judul
   ↓
Video Cut
   ↓
Rename Video
   ↓
Generate Subtitle
```

---

# Project Structure

```
clipper_toolkit/

LICENSE
README.md
requirements.txt
.gitignore

clipper_tools.py

scripts/
  extractor.py
  video_cut.py
  rename_video.py
  subtitle_generator.py

sample/
  example_input.txt

data/
  .gitkeep

output/
  clips/
    .gitkeep
```

Folder penting:

* **scripts/** → semua tool utama
* **sample/** → contoh input extractor
* **data/** → hasil extractor (timestamp & judul)
* **output/clips/** → hasil potongan video dan subtitle

---

# Requirements

* Python 3.9+
* FFmpeg
* GPU opsional (untuk Whisper lebih cepat)

Install Python dependencies:

```
pip install -r requirements.txt
```

---

# Install FFmpeg

Tool pemotong video menggunakan FFmpeg.

Download dari:

https://ffmpeg.org/download.html

Pastikan sudah terinstall dengan menjalankan:

```
ffmpeg -version
```

---

# Cara Menjalankan

Masuk ke folder project lalu jalankan:

```
python clipper_tools.py
```

Menu toolkit akan muncul:

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

# Cara Menggunakan

### 1️⃣ Extract Timestamp

Gunakan file teks yang berisi timestamp dan judul.

Contoh file tersedia di:

```
sample/sample_input.txt
```

Ketika memilih menu **Extract Timestamp**, masukkan path file tersebut:

```
sample/sample_input.txt
```

Output yang dihasilkan:

```
data/timestamp.txt
data/judul.txt
```

---

### 2️⃣ Potong Video

Pilih menu:

```
2. Potong Video
```

Masukkan path video sumber, contoh:

```
D:\video\podcast.mp4
```

Script akan membaca:

```
data/timestamp.txt
```

Lalu menghasilkan clip:

```
output/clips/clip_1.mp4
output/clips/clip_2.mp4
```

Jika timestamp melebihi durasi video, clip tersebut akan **di-skip otomatis**.

---

### 3️⃣ Rename Video

Pilih menu:

```
3. Rename Video
```

Clip akan diubah namanya berdasarkan isi:

```
data/judul.txt
```

Contoh:

```
clip_1.mp4
↓
NPC_ini_tiba_tiba_melakukan_hal_absurd.mp4
```

---

### 4️⃣ Generate Subtitle

Pilih menu:

```
4. Generate Subtitle
```

Pilih:

* bahasa transkripsi
* model Whisper

Contoh model:

| Model  | Speed         | Akurasi      |
| ------ | ------------- | ------------ |
| tiny   | sangat cepat  | rendah       |
| base   | cepat         | cukup        |
| small  | seimbang      | bagus        |
| medium | lambat        | sangat bagus |
| large  | paling lambat | terbaik      |

Subtitle `.srt` akan dibuat di folder yang sama dengan video:

```
output/clips/
```

Contoh hasil:

```
NPC_ini_tiba_tiba_melakukan_hal_absurd.mp4
NPC_ini_tiba_tiba_melakukan_hal_absurd.srt
```

---

# Catatan

* Model Whisper akan otomatis diunduh saat pertama kali digunakan.
* Model yang lebih besar memberikan akurasi lebih tinggi tetapi membutuhkan RAM/VRAM lebih besar.
* Jika GPU tersedia, proses transkripsi akan jauh lebih cepat.

---

# License

Proyek ini menggunakan **MIT License**.

Lihat file `LICENSE` untuk detail lengkap.
