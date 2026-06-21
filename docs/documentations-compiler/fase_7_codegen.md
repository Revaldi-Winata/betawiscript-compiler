# Dokumentasi Fase 7: Code Generation & Packaging

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil_&_Aman-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 7: Code Generation & Packaging** dari kompilator BetawiScript.

## Apa itu Fase 7 (Code Generation)?
Fase 7 (Code Generation & Packaging) adalah babak penutup jalur kompilasi di mana AST yang telah lolos analisis dan dioptimalkan diterjemahkan sepenuhnya ke lingkungan instruksi target (mesin Python 3), dan dipaketkan ke dalam file aplikasi (*Standalone Binary Executable*).

## Rincian Implementasi
Implementasi pada fase ini memecah proses menjadi dua area kerja yang selaras:
- **Konstruksi Target:** Modul `CodeGenerator` (di `src/codegen.py`) menterjemahkan kembali instruksi hierarkis AST dari modul BetawiScript untuk membangun skrip Python string yang diakomodasikan dengan struktur indentasi spasial secara akurat.
- **Pengepakan Biner:** Menggunakan modul `PyInstaller` yang dikonfigurasi melalui sistem antarmuka command-line `betawi.py` (via argumen `rilis`) untuk membungkus program utuh menjadi file portabel tunggal (`.exe`), mendistribusikan pustaka secara terisolasi.

## Hasil Validasi
Berdasarkan uji *Black Box* dan verifikasi *end-to-end* operasional:
1. Skrip berekstensi `.betawi` kini berhasil ditranskripsikan tanpa kesalahan dan dieksekusi melalui antarmuka Windows Shell PowerShell secara murni tanpa mewajibkan *user* menginstal perantara *runtime environment* sistem operasi.
2. Perintah `betawi.exe rilis` telah dibuktikan kompeten dalam menopang pembuatan sub-aplikasi yang 100% *standalone*.
3. Lolos uji *Automated Black Box Testing* (*Pass Rate:* **100%**).

---
*Terakhir Diperbarui: 2026-06-08*
