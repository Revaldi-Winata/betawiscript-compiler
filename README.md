# BetawiScript Mini Compiler

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![Lisensi](https://img.shields.io/badge/Lisensi-MIT-green?style=for-the-badge)
![Versi](https://img.shields.io/badge/Versi-1.0.0-blue?style=for-the-badge)

**BetawiScript** adalah sebuah dialek bahasa pemrograman eksperimental yang mengadopsi sintaksis Python namun dengan kearifan lokal bahasa Betawi. 

</div>

---

BetawiScript Mini Compiler adalah proyek kompilator berukuran kecil yang dibangun sebagai eksperimen dan implementasi praktikum untuk ranah ilmu Teknik Kompilasi. Proyek ini mendemonstrasikan bagaimana tahapan kompilasi perangkat lunak dilakukan dari hulu ke hilir, mulai dari proses *Lexical Analysis* hingga *Code Generation*.

Perlu dicatat bahwa kompilator ini merupakan **murni sebuah bahasa *mini*** yang menargetkan dan mendukung **subset kata kunci** serta operasi prosedural dasar untuk memvalidasi alur teori kompilasi, bukan untuk menggantikan bahasa pemrograman skala enterprise secara menyeluruh.

## Fitur Utama

- **Sintaks Lokal Betawi Dasar**: Mendukung kata kunci pemrograman esensial yang diubah ke bahasa Betawi (seperti `bikin` untuk mendefinisikan fungsi, `kalo` untuk kondisi logika, `selagi` untuk perulangan). Rujukan lengkap terdapat pada file [REFERENSI_BAHASA.md](REFERENSI_BAHASA.md).
- **Standalone Binary**: Dilengkapi dengan pengaturan pemaketan sehingga dapat didistribusikan sebagai satu file `betawi.exe` yang langsung dapat dijalankan di ekosistem Windows.
- **Pipeline Kompilasi Murni**: Alur kerja menerapkan arsitektur kompilator klasik:
  - Fase 1: Desain Bahasa & Pemetaan Kata Kunci
  - Fase 2: Penganalisis Leksikal (*Lexer*)
  - Fase 3: Penganalisis Sintaksis (*Parser*)
  - Fase 4: Pembangun Abstract Syntax Tree (*AST Builder*)
  - Fase 5: Penganalisis Semantik (*Semantic Analyzer*)
  - Fase 6: Optimasi AST (*Constant Folding*, *Dead Code Elimination*)
  - Fase 7: Pembangkit Kode (*Code Generator*)

## Panduan Penggunaan `betawi.exe`

Bagi pengguna yang sudah memiliki file `betawi.exe`, program ini dapat dijalankan langsung melalui *Command Prompt* atau *PowerShell* di Windows **tanpa memerlukan instalasi Python**.

### Persiapan Direktori & Environment Variables PATH
Agar eksekusi lancar, disarankan mendaftarkan direktori penyimpanan kompilator ke dalam *Environment Variables PATH* Windows:
1. Buka *Start Menu* Windows, ketik **Edit the system environment variables**, lalu tekan *Enter*.
2. Klik tombol **Environment Variables...**.
3. Pada area *System variables*, pilih variabel bernama **Path**, lalu klik **Edit...**
4. Klik **New**, lalu tempel (*paste*) jalur folder tempat `betawi.exe` berada.
5. Klik **OK** untuk menyimpan perubahan.

### Menjalankan Skrip
Perintah `jalan` digunakan untuk mengeksekusi file kode berekstensi `.betawi` secara langsung.
```bash
betawi jalan (nama_file).betawi
```

### Membangun Aplikasi Baru (Pemaketan Rilis)
Perintah `rilis` digunakan untuk mengompilasi dan memaketkan skrip `.betawi` menjadi sebuah **aplikasi `.exe` mandiri** yang *portable* dan tidak bergantung pada `betawi.exe` itu sendiri.
```bash
betawi rilis (nama_file).betawi
```

## Setup Builder (Membangun Ulang Kompilator)

Jika ada pembaruan pada mesin inti kompilator, file `betawi.exe` dapat dibangun ulang melalui skrip utama `betawi.py` menggunakan `PyInstaller`. Pembuatan ini disarankan dilakukan di dalam **lingkungan virtual Python (Virtual Environment) yang bersih**.

1. Instalasi pustaka pembuat file eksekusi:
   ```bash
   pip install pyinstaller
   ```
2. Bangun program melalui perintah berikut:
   ```bash
   pyinstaller --onefile --name betawi betawi.py
   ```
Hasil kompilasi mesin akan tersimpan otomatis di dalam direktori `dist/`.

## Pengujian (Testing)

Proyek ini mendefinisikan beberapa lapisan pengujian (*testing*) untuk membuktikan integritas kompilator. Setiap tahap kompilator diuji secara terpisah (*Unit Testing*) serta diuji secara fungsional penuh (*End-to-End Testing*).

Eksekusi rangkaian pengujian dapat dilakukan menggunakan modul unittest bawaan Python:
```bash
python -m unittest discover tests
```

### Strategi Pengujian:
1. **Fase Pengujian Terisolasi**: Setiap file `test_*.py` mengevaluasi masing-masing lapisan (`lexer`, `parser`, `ast`, `semantic`, `optimizer`, `codegen`) untuk memastikan tidak ada kesalahan input/output pada setiap komponen.
2. **Stress Testing (Beban Kompilasi)**: Modul optimasi akan mereduksi operasi aritmatika yang panjang sehingga memori efisien.
3. **Negative Testing**: Memastikan mesin kompilator menangkap kesalahan gramatikal seperti kurung kurawal yang kurang dan mengembalikan log kesalahan secara prediktif tanpa memicu *crash* internal sistem.

## Struktur Repositori

```text
betawiscript-compiler/
│
├── docs/                     # Dokumentasi mendalam per-fase kompilator
├── src/                      # Modul Inti Kompilator (Leksikal hingga Code Gen)
├── tests/                    # Direktori Unit Testing dan Full Coverage
├── betawi.py                 # File Utama (Builder / CLI Setup)
├── trace_compiler.py         # Skrip Diagnostik & Debugging Terminal
├── REFERENSI_BAHASA.md       # Daftar Kosakata BetawiScript
├── README.md                 # Dokumentasi Proyek Ini
└── dist/
    └── betawi.exe            # Aplikasi Kompilator Mandiri (Binary)
```

---

> **Catatan Pengembang**: Penulis bukanlah penutur asli bahasa Betawi. Jika terdapat penggunaan kosakata atau istilah sintaksis Betawi yang kurang tepat atau tidak sesuai dengan kaidah budaya aslinya, silakan *fork* repositori ini dan perbaiki secara mandiri.