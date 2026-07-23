# 🎬 Clipper Toolkit

Toolkit Python untuk workflow **video clipping otomatis** — dari ekstraksi timestamp, pemotongan video, rename clip, hingga generate subtitle menggunakan Whisper AI.

Dirancang untuk mempercepat pembuatan **short-form content** (YouTube Shorts, TikTok, Reels) dari video panjang.

---

## ✨ Fitur

- 📄 Extract **timestamp dan judul** otomatis dari file teks
- ✂️ Potong video berdasarkan timestamp menggunakan FFmpeg
- 🏷️ Rename clip otomatis berdasarkan judul
- 🎙️ Generate subtitle `.srt` menggunakan **OpenAI Whisper**
- ⚡ Deteksi GPU otomatis (CUDA jika tersedia, fallback ke CPU)
- 🔁 Skip otomatis jika file `.srt` sudah ada

---

## 🗂️ Struktur Folder

```
Clipper-Tools/
│
├── clipper_tools.py          ← Entry point utama (menu interaktif)
├── requirements.txt
├── README.md
│
├── scripts/
│   ├── extractor.py          ← Extract timestamp + judul dari teks
│   ├── video_cut.py          ← Potong video pakai FFmpeg
│   ├── rename_video.py       ← Rename clip berdasarkan judul
│   └── subtitle_generator.py ← Generate .srt pakai Whisper
│
├── data/                     ← Output extractor (diisi otomatis)
│   ├── timestamp.txt
│   ├── hook.txt
│   └── Super_Title.txt
│
├── output/
│   └── clips/                ← Hasil clip video + file .srt
│
└── sample/
    └── sample_input.txt      ← Contoh format file input
```

---

## ⚙️ Requirements

- Python **3.11** atau **3.12** (direkomendasikan untuk GPU support)
- FFmpeg (diinstall terpisah di sistem)
- GPU NVIDIA + CUDA *(opsional, untuk Whisper lebih cepat)*

> ⚠️ **Catatan:** Python 3.14 saat ini hanya mendukung PyTorch versi CPU-only.
> Gunakan Python 3.11 atau 3.12 agar GPU bisa digunakan.

---

## 🚀 Instalasi

### 1. Install Python 3.11 atau 3.12

Download dari [python.org](https://www.python.org/downloads/) dan centang **"Add to PATH"** saat instalasi.

```bash
py --list
# Pastikan Python 3.11 atau 3.12 muncul di list
```

### 2. Install FFmpeg

Download dari [ffmpeg.org](https://ffmpeg.org/download.html) dan tambahkan ke PATH sistem.

```bash
ffmpeg -version
# Pastikan perintah ini berhasil dijalankan
```

### 3. Buat Virtual Environment

```bash
# Masuk ke folder project
cd Clipper-Tools

# Buat venv dengan Python 3.11
py -3.11 -m venv venv

# Aktifkan venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 4. Install PyTorch dengan CUDA (GPU)

> Install PyTorch CUDA **terlebih dahulu** sebelum library lain.

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu132
```

> 💡 Sesuaikan `cu132` dengan versi CUDA yang didukung driver GPU kamu (cek dengan `nvidia-smi`, lihat kolom "CUDA Version" di pojok kanan atas). Index yang tersedia saat ini antara lain `cu126`, `cu130`, `cu132`.
>
> ⚠️ Tidak perlu install `torchaudio` — project ini load audio lewat FFmpeg (bukan torchaudio), dan beberapa index CUDA terbaru sudah tidak menyediakan wheel torchaudio.

Verifikasi GPU terdeteksi:

```bash
python -c "import torch; print(torch.cuda.is_available())"
# Output: True
```

Jika tidak punya GPU atau ingin pakai CPU saja:

```bash
pip install torch torchvision torchaudio
```

### 5. Install Library Lainnya

```bash
pip install openai-whisper ffmpeg-python numpy tqdm
```

---

## ▶️ Cara Menjalankan

Pastikan venv sudah aktif, lalu jalankan:

```bash
python clipper_tools.py
```

Menu interaktif akan muncul:

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

## 📋 Alur Kerja

```
File Teks (timestamp + judul)
         ↓
  1. Extract Timestamp + Judul
         ↓
  2. Potong Video  ──────────── input: video sumber
         ↓
  3. Rename Video
         ↓
  4. Generate Subtitle
         ↓
  output/clips/  ──────────── clip_01_judul.mp4 + .srt
```

---

## 📖 Panduan Penggunaan

### 1️⃣ Extract Timestamp + Judul

Siapkan file teks dengan format seperti contoh di `sample/sample_input.txt`.

Pilih menu **1**, lalu masukkan path file teks:

```
sample/sample_input.txt
```

Output yang dihasilkan di folder `data/`:

| File | Isi |
|------|-----|
| `timestamp.txt` | Pasangan waktu start - end |
| `hook.txt` | Deskripsi singkat setiap clip |
| `Super_Title.txt` | Judul utama setiap clip |

---

### 2️⃣ Potong Video

Pilih menu **2**, lalu masukkan path video sumber:

```
D:\video\podcast.mp4
```

Script membaca `data/timestamp.txt` dan menghasilkan clip di `output/clips/`:

```
output/clips/clip_1.mp4
output/clips/clip_2.mp4
...
```

---

### 3️⃣ Rename Video

Pilih menu **3**. Clip akan diubah namanya berdasarkan `data/Super_Title.txt`:

```
clip_1.mp4  →  01_Judul_Video_Pertama.mp4
clip_2.mp4  →  02_Judul_Video_Kedua.mp4
```

---

### 4️⃣ Generate Subtitle

Pilih menu **4**, lalu pilih:

- Bahasa transkripsi (Indonesia / Inggris)
- Model Whisper

| Model | Kecepatan | Akurasi | VRAM |
|-------|-----------|---------|------|
| tiny | Sangat cepat | Rendah | ~1 GB |
| base | Cepat | Cukup | ~1 GB |
| small | Seimbang | Bagus | ~2 GB |
| medium | Lambat | Sangat bagus | ~5 GB |
| large | Paling lambat | Terbaik | ~10 GB |

File `.srt` akan dibuat di folder yang sama dengan video:

```
output/clips/01_Judul_Video_Pertama.mp4
output/clips/01_Judul_Video_Pertama.srt  ← dibuat otomatis
```

> 💡 Jika file `.srt` sudah ada, file tersebut akan di-skip otomatis.

---

## 📝 Catatan

- Model Whisper didownload otomatis saat pertama kali digunakan dan disimpan di cache sistem (`~/.cache/whisper/`). Venv baru tidak perlu download ulang.
- Gunakan model `small` atau `medium` untuk keseimbangan antara kecepatan dan akurasi.
- Jika GPU tidak tersedia, proses berjalan di CPU (lebih lambat, terutama untuk model besar).

---

## 📄 License

Proyek ini menggunakan **MIT License** — lihat file `LICENSE` untuk detail.
