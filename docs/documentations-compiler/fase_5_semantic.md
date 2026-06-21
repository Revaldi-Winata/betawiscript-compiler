# Dokumentasi Fase 5: Semantic Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil_&_Aman-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 5: Semantic Analysis** dari kompilator BetawiScript.

## Apa itu Fase 5 (Semantic Analysis)?
Fase 5 (Semantic Analysis) adalah sistem pemeriksa keabsahan dan kebenaran makna dari kode yang ada di dalam *Abstract Syntax Tree (AST)*, bertugas memastikan bahwa alur logika yang dirangkai masuk akal dan memenuhi hukum komputasi (seperti melarang penggunaan variabel yang belum dideklarasikan).

## Rincian Implementasi
Sistem semantik dibangun menggunakan modul `SemanticAnalyzer` (dalam berkas `src/semantic.py`) yang mengaplikasikan penelusuran berulang (Visitor Pattern) melintasi setiap *node* AST.

Sistem ini sangat mengandalkan komponen keamanan *Symbol Table* dalam melacak ruang lingkup (*Scope*). Setiap kali penelusur memasuki blok logika bersarang (seperti di dalam iterasi atau fungsi), operasi memori `push_scope` akan aktif, lalu ditutup dengan `pop_scope` begitu keluar dari kurung kurawal `{ }`.

## Hasil Validasi
Menurut laporan performa di berkas `tests/test_semantic.py`:
1. Sistem sukses menangkap pelemparan pengecualian (*exception*) kelas `SemanticError` ketika skrip mencoba menyalahgunakan ruang lingkup memori.
2. Mesin analitik mampu menemukan dan melaporkan lokasi baris tempat variabel yang tidak valid dengan akurasi **100%**.
3. Tingkat keberhasilan validasi otomatis (Automated Unit Tests) adalah penuh tanpa kegagalan satupun.

---
*Terakhir Diperbarui: 2026-06-08*
