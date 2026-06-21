# Dokumentasi Fase 1: Desain Bahasa

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 1: Desain Bahasa** dari kompilator BetawiScript.

## Apa itu Fase 1 (Desain Bahasa)?
Fase 1 (Desain Bahasa) adalah tahapan awal pembuatan kompilator yang bertujuan untuk menetapkan spesifikasi inti bahasa BetawiScript, merancang substitusi dari kosakata bahasa pemrograman Python menjadi representasi lokal Betawi.

## Rincian Implementasi
Pada tahap ini, pengembangan difokuskan pada pemetaan tata bahasa:

- **Kata Kunci Kontrol:** Telah ditetapkan pemetaan 35 kata kunci kontrol utama (contohnya `kalo`, `bikin`, `selagi`).
- **Fungsi Bawaan:** Telah ditetapkan pemetaan 68 fungsi bawaan (contohnya `cetak`, `nanya`).
- **Context-Free Grammar (CFG):** Telah dirumuskan struktur tata bahasa sederhana yang menjadi pondasi pembentukan pohon sintaksis pada fase parser dan compiler selanjutnya.

Menurut arsitektur sistem, karena bahasa ini dirancang eksklusif sebagai subset fungsional untuk eksperimen teknik kompilasi, tipe data kompleks atau fitur orientasi objek sengaja tidak didukung. Fokus dialihkan sepenuhnya pada aliran logika prosedural dasar.

## Hasil Validasi
1. Terjemahan kosa kata berhasil terdaftar secara penuh ke dalam dokumentasi **REFERENSI_BAHASA.md**.
2. Hasil perancangan tata bahasa sukses digunakan sebagai fondasi mutlak bagi komponen Lexer (`token.py`) dalam melakukan eksekusi pengenalan karakter tanpa *error*.

---
*Terakhir Diperbarui: 2026-06-08*
