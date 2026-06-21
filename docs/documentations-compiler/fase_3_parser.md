# Dokumentasi Fase 3: Parser (Analisis Sintaksis)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil_&_Aman-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 3: Parser** dari kompilator BetawiScript.

## Apa itu Fase 3 (Parser)?
Fase 3 (Parser) adalah tahapan analisis sintaksis yang menerima aliran Token dari Lexer dan merakitnya menjadi sebuah pohon struktural yang disebut *Parse Tree* atau *Concrete Syntax Tree (CST)*, guna memverifikasi bahwa urutan token sesuai dengan aturan Context-Free Grammar.

## Rincian Implementasi
Parser ini dirakit murni menggunakan algoritma rekursif **Recursive Descent Parsing**. Pada fase ini, sistem tidak melakukan modifikasi atau reduksi apapun (bersifat struktural penuh). Semua karakter, termasuk tanda baca dekoratif seperti kurung dan titik dua, disimpan secara eksplisit di dalam Tree.

File yang digunakan dalam eksekusi ini:
- `src/cst_nodes.py`: Mendefinisikan class `ParseNode` untuk pembentukan *tree* hierarkis bersarang dan modul pencetak (*printer*) visual.
- `src/parser.py`: Engine *Recursive Descent* Parser lengkap yang menangani Presedensi Operator Matematika, Blok Kode, Percabangan (`kalo`, `kalo_lain`, `lainnyo`), Perulangan, dan Pemanggilan Fungsi.

## Hasil Validasi
Berdasarkan metrik pengujian di `tests/test_parser.py`:
1. **Tingkat Kelulusan:** 100% *Pass* pada seluruh 4 kasus uji coba kompleks.
2. **Waktu Respons:** Total waktu eksekusi validasi memakan waktu **0.002 detik**.
3. **Pencetakan Visual:** Algoritma Parser mampu merepresentasikan pohon bersarang (nested) sempurna, misalnya `x = (2 + 3) * 5`, membuktikan integritas hirarkis bekerja tanpa interupsi kesalahan sintaksis.

---
*Terakhir Diperbarui: 2026-06-08*
