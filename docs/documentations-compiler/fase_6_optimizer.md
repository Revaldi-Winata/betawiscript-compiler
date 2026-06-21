# Dokumentasi Fase 6: Code Optimization

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil_&_Aman-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 6: Code Optimization** dari kompilator BetawiScript.

## Apa itu Fase 6 (Code Optimization)?
Fase 6 (Code Optimization) adalah tahap pasca-semantik yang bertugas menganalisis dan memodifikasi ranting pohon AST secara otonom untuk memangkas proses kalkulasi redundan, mengurangi ukuran instruksi, dan meningkatkan kecepatan eksekusi akhir *runtime*.

## Rincian Implementasi
Modul pengoptimalan dijalankan melalui `src/optimizer.py` (`ASTOptimizer`) menggunakan mode *post-order traversal* untuk memodifikasi struktur pohon mulai dari lapisan terbawah (daun) ke lapisan tertinggi (akar).

Pilar optimasi yang diaplikasikan:
- **Constant Folding:** Secara otomatis memecahkan operasi aritmatika statis (seperti penjumlahan `5 + 5` atau operasi boolean `Bana dan Salah`) langsung saat waktu kompilasi (*compile-time*), mengubahnya menjadi representasi konstanta mutlak agar mesin tidak membuang daya pemrosesan CPU di *runtime*.
- **Dead Code Elimination:** Mampu mendeteksi secara proaktif jalur kode yang tidak akan pernah tereksekusi secara teoritis (contoh: blok if dengan kondisi absolut `Salah`) dan menghapus rutenya secara langsung dari AST.

## Hasil Validasi
Pada skenario *Stress Testing* (Beban Skala Besar) yang memuat puluhan ribu injeksi aritmatika berurutan (`test_optimizer.py`):
1. **Keberhasilan Proteksi:** Aplikasi tidak membeku (*crash*) akibat tumpukan memori (*Stack Overflow*).
2. **Efisiensi:** Pohon AST yang sangat dalam berhasil direduksi secara drastis hingga **lebih dari 90%** ukuran aslinya dan menghasilkan keluaran instan dalam hitungan **milidetik**.

---
*Terakhir Diperbarui: 2026-06-08*
