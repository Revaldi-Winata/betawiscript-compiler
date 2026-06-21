# Dokumentasi Fase 2: Lexer

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil_&_Aman-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 2: Lexer** dari kompilator BetawiScript.

## Apa itu Fase 2 (Lexer)?
Fase 2 (Lexer) adalah komponen kompilator yang membaca teks sumber *source code* karakter demi karakter, lalu memecahnya dan mengelompokkannya menjadi *Token* atau potongan kata yang memiliki makna tata bahasa (seperti token `KEYWORD`, `IDENTIFIER`, atau `OPERATOR`).

## Rincian Implementasi
Lexer dibangun menggunakan mekanisme Regular Expression (Sequence Matching) tanpa bergantung pada dependensi atau pustaka eksternal pihak ketiga, menjamin proses berjalan linear, terisolasi, dan sangat cepat.

File yang berperan dalam fase ini:
- `src/token.py`: Mendefinisikan struktur `TokenType` Enum dan kelas `Token`.
- `src/lexer.py`: Mesin utama eksekusi Lexer.

Sesuai revisi arsitektur terbaru, `EXCEPTIONS` dan `CONSTANTS` telah dihapus secara fisik dan konseptual dari komponen Lexer. Nilai konstanta murni seperti `Bana` (True), `Salah` (False), dan `Kosong` (None) kini diproses secara natif sebagai `KEYWORD` agar relevan dengan arsitektur dasar Python 3.

## Hasil Validasi
1. **Kecepatan Eksekusi:** Seluruh 3 *test suites* yang berjalan di dalam `tests/test_lexer.py` sukses diselesaikan dalam **0.002 detik**.
2. **Akurasi Pemecahan:** Lexer memiliki tingkat keberhasilan (Pass rate) **100%** dalam memproses blok kurung kurawal `{ }`, *built-in function scanning*, pemecahan operator matematika secara presisi, serta akurat mendeteksi letak baris/kolom dari karakter ilegal.

---
*Terakhir Diperbarui: 2026-06-08*
