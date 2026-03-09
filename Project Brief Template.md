---

### **Informasi Peserta**

| No  |      Nama      | Email Dicoding  |
| :-: | :------------: | :-------------: |
|  1  |  [Nama Anda]   |  [Email Anda]   |
|  2  | [Nama Anggota] | [Email Anggota] |
|  3  | [Nama Anggota] | [Email Anggota] |

- ### **Problem Statement**

Banjir merupakan salah satu bencana alam yang paling sering terjadi di Indonesia, yang seringkali disebabkan oleh curah hujan ekstrem pada musim penghujan. Kurangnya sistem peringatan dini yang akurat, informatif, dan mudah diakses oleh masyarakat umum maupun pemangku kebijakan sering kali mengakibatkan keterlambatan penanganan dan evakuasi, sehingga menimbulkan kerugian material hingga korban jiwa. Oleh karena itu, dibutuhkan sebuah solusi berbasis data cerdas yang tidak hanya memprediksi cuaca, tetapi juga mengklasifikasikan tingkat risiko banjir serta memberikan rekomendasi tindakan secara real-time.

- ### **Deskripsi Produk/Aplikasi**

**RainGuard AI** adalah sebuah platform Sistem Peringatan Dini Risiko Banjir berbasis kecerdasan buatan (Artifical Intelligence). Sistem ini memanfaatkan model _Long Short-Term Memory_ (LSTM) untuk memprediksi curah hujan harian berdasarkan data multi-variat, serta mengambil data cuaca secara _real-time_ dari BMKG secara langsung untuk ke-34 provinsi di Indonesia. RainGuard AI mengolah keluaran model menjadi sebuah klasifikasi tingkat ancaman banjir (Rendah, Sedang, Tinggi) dan merepresentasikan wawasannya melalui _dashboard_ interaktif yang dilengkapi dengan rekomendasi tindakan mitigasi dan peta visual genangan berbasis 3D.

- ### **Fitur Utama dan Teknologi yang Digunakan**

Berikut adalah penjabaran fitur-fitur dan teknologi utama yang menyusun RainGuard AI:

- **Generasi Dataset & Pipeline Pra-pemrosesan Data (Pandas & Numpy)**: Skrip ETL menghasilkan sintesis 74.500+ catatan data prakiraan cuaca musiman di Indonesia sebagai langkah awal pelatihan simulasi AI.
- **Prediksi Cuaca Cerdas (PyTorch LSTM)**: Model jaringan saraf tiruan (Deep Learning) dilatih untuk memprediksi probabilitas dan curah hujan dalam jangka 3 hingga 14 hari ke depan.
- **Integrasi Cuaca Real-time BMKG (BeautifulSoup)**: Fetcher _Open Data_ sinkron secara langsung dengan API XML BMKG guna memberikan status meteorologi terkini di 34 provinsi seluruh Indonesia.
- **Sistem Keputusan Penilaian Risiko AI**: Sebuah mesin klasifikasi dinamis yang mengonversi angka prakiraan milimeter hujan menjadi tingkat peringatan dini bencana dan tips mitigasi (Evakuasi/Siaga).
- **Backend API Tangguh (FastAPI & Uvicorn)**: Menyediakan arsitektur infrastruktur _server-side_ yang melayani request secara cepat (REST API Endpoint `/predict`).
- **Frontend Dashboard Interaktif (Streamlit & Plotly)**: Antarmuka cantik berbasis _glassmorphism_ untuk menyajikan data AI ke tangan pengguna.
- **Pemetaan Topologis Canggih (PyDeck)**: Menggunakan teknologi visualisasi scatter-plot spasial 3D untuk memvisualisasikan konsentrasi dan kepadatan luas genangan di titik-titik daerah rawan tiap provinsi.

- ### **Cara Penggunaan Product**

Produk didesain sedemikian rupa agar masyarakat umum atau pengguna _early-user_ dapat menggunakan aplikasi RainGuard AI secara intuitif. Aplikasi terintegrasi secara monolitik (tanpa perlu repot menyalakan backend terpisah). Jalankan perintah instalasi dan server di bawah ini:

1. Buka terminal (pastikan virtual environment Python Anda sudah aktif).
2. **Jalankan Web Dashboard:** Ketik dan jalankan perintah `streamlit run app/streamlit_app.py`.
3. Buka URL Web Streamlit pada browser (biasanya `http://localhost:8501`).
4. Pada panel sebelah kiri (**Sidebar Konfigurasi**), pengguna dapat menekan _dropdown_ untuk **memilih target dari 34 Provinsi di Indonesia**.
5. Sesuaikan parameter jumlah hari prakiraan (contoh: 7 Hari ke Depan).
6. Klik tombol biru **"Prediksi Risiko Banjir"** untuk menembak query ke AI secara _on-the-fly_.
7. _Dashboard_ secara instan akan memuat status klasifikasi bahaya banjir terbaru, kondisi _real-time_ cuaca berdasarkan pengolahan data BMKG resmi, serta melukis matriks visual bar-plot Plotly.
8. Pengguna bisa membaca **Rekomendasi Tindakan** mitigasi di sebelah kanan. Pengguna juga dapat mulai berinteraksi dengan peta visualisasi persebaran 3D di bagian bawah yang secara dinamis merefleksikan keparahan rintik/genangan topologis menggunakan pustaka pydeck.

- ### **Informasi Pendukung [Opsional]**

**Tautan Penting & Dokumentasi:**

- **Repository GitHub:** [Link GitHub Anda Di Sini]
- **Demo Video (YouTube/Lainnya):** [Link Video Demo Anda Di Sini]
- **Live App (Streamlit Cloud):** [Link Streamlit App Anda Di Sini]
- Proyek _repository_ mencakup arsip interaktif eksplorasi _raw data_ yang digarap menggunakan antarmuka Jupyter Notebook `training_model.ipynb`.
- Seluruh arsitektur _dependency_ dapat sepenuhnya direplikasi menggunakan berkas virtual environment _modern package manager_ (seperti `uv` atau `pip`).

**Rencana Pengembangan ke Depan:**

1. **Penggunaan Data Historis Asli:** Saat ini, model LSTM dilatih menggunakan sintesis 74.500+ titik data. Ke depannya, bekerja sama dengan pemangku kebijakan (seperti BNPB/BMKG) untuk mengintegrasikan data cuaca historis yang valid akan menghasilkan _tuning_ parameter prediksi yang jauh lebih presisi.
2. **Aplikasi Mobile (iOS/Android):** Pembuatan portal aplikasi peringatan dini khusus _mobile_ berbasis Flutter/React Native, memanfaatkan REST API FastAPI yang telah dikembangkan secara parsial.
3. **Sistem Notifikasi Pusher (Push Notifications):** Mengotomatiskan peringatan via WhatsApp API atau Email Blast kepada penduduk di wilayah tertentu jika titik ambang batas peringatan (Warna Merah / High Risk) telah dilampaui.
4. **Hiperlokalisasi Radar Geo-spasial:** Meningkatkan skala resolusi prediksi genangan dari tingkat provinsi menjadi tingkat kecamatan atau grid spesifik (1x1 km) guna mempercepat koordinasi rute evakuasi.
