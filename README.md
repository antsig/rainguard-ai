# RainGuard AI

Sistem Peringatan Dini Risiko Banjir Berbasis AI

## Gambaran Umum

RainGuard AI adalah aplikasi ringkas yang dirancang untuk membantu masyarakat bersiap menghadapi potensi bencana banjir dengan memberikan peringatan dini berdasarkan prediksi curah hujan menggunakan Kecerdasan Buatan (AI).

Sistem ini memprediksi curah hujan untuk beberapa hari ke depan dan mengklasifikasikan tingkat risiko banjir untuk membantu orang mengambil tindakan pencegahan.

## Masalah

Indonesia adalah salah satu negara paling rawan bencana di dunia. Banjir adalah salah satu bencana paling umum yang disebabkan oleh curah hujan ekstrem.

Masyarakat sering kali menerima peringatan terlambat untuk bersiap.

## Solusi

RainGuard AI menyediakan:

- Prediksi curah hujan menggunakan AI
- Klasifikasi risiko banjir
- Rekomendasi kesiapsiagaan

## Fitur

- Prediksi Curah Hujan (1–7 hari ke depan)
- Klasifikasi Risiko Banjir
- Dashboard Peringatan Dini Interaktif
- Rekomendasi Tindakan Kesiapsiagaan
- **[Baru]** Integrasi Cuaca Real-Time Terkini dari BMKG (Parsing XML Terbuka)
- **[Baru]** Peta Peringatan Genangan Banjir 2D/3D Interaktif (Simulasi PyDeck Koordinat Detail Area)

## Model AI

Modified LSTM (Temporal Sequence Prediction)

Fitur masukan:

- Riwayat curah hujan
- Fitur waktu (Time features)
- Indikator cuaca

Keluaran:

- Prediksi curah hujan

## Teknologi yang Digunakan

- Python
- PyTorch
- Streamlit
- FastAPI
- Beautifulsoup4 & lxml (Web Scraping BMKG)
- Plotly & PyDeck

## Cara Menjalankan Aplikasi dari Awal (Langkah demi Langkah)

Pastikan Anda memiliki [Python 3.9+](https://www.python.org/downloads/) terinstal di sistem Anda.

### 1. Clone Repository & Setup Virtual Environment

Buka terminal/Command Prompt dan jalankan:

```bash
# Clone repository
git clone https://github.com/username/rainguard-ai
cd rainguard-ai

# Opsional namun disarankan: Buat virtual environment
python -m venv venv

# Aktifkan virtual environment (Windows)
venv\Scripts\activate
# (Mac/Linux: source venv/bin/activate)

# Install semua dependency
pip install -r requirements.txt
```

### 2. Generate Data Sintetis

Sistem ini membutuhkan data cuaca historis. Karena tidak menggunakan data langsung dari BMKG untuk demonstrasi, kita akan men-generate data sintetis:

```bash
python src/generate_data.py
```

_(Ini akan membuat file `data/rainfall_dataset.csv` dengan 5 tahun data cuaca untuk berbagai kota)_

### 3. Training Model AI (LSTM)

Latih model machine learning menggunakan data yang baru dibuat:

```bash
python src/train_model.py
```

_(Tunggu hingga proses training 10 epochs selesai. Model akan disimpan di `models/lstm_model.pth`)_

### 4. Jalankan Early Warning Dashboard (Streamlit)

Buka terminal (pastikan virtual environment aktif), lalu jalankan:

```bash
streamlit run app/streamlit_app.py
```

_(Browser akan otomatis membuka dashboard interaktif dan peta risiko banjir di http://localhost:8501. Aplikasi terintegrasi secara monolitik, yang berarti Model AI (PyTorch) akan dijalankan seketika di peranti Anda tanpa memerlukan backend tambahan.)_

## Dampak

RainGuard AI membantu masyarakat:

- Mengantisipasi curah hujan lebat
- Bersiap menghadapi potensi banjir
- Meningkatkan kesiapsiagaan bencana

## Rencana Pengembangan Selanjutnya

- Aplikasi Peringatan Dini Berbasis iOS/Android Mobile
- Sistem _Push Notification_ (WhatsApp/Email API) saat status Bahaya (Merah) tercapai.
