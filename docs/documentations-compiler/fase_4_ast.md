# Dokumentasi Fase 4: Abstract Syntax Tree (AST)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Selesai-success?style=for-the-badge) ![Keamanan](https://img.shields.io/badge/Keamanan-Stabil_&_Aman-success?style=for-the-badge)

> **Konteks:** Dokumen ini menjelaskan rancangan, implementasi, dan validasi untuk **Fase 4: Abstract Syntax Tree** dari kompilator BetawiScript.

## Apa itu Fase 4 (AST)?
Fase 4 (AST) adalah proses penyederhanaan pohon *Concrete Syntax Tree (CST)* yang mentah dengan cara membuang seluruh karakter non-esensial dan elemen dekoratif sintaks (seperti tanda kurung dan titik koma), sehingga menghasilkan struktur logika murni yang ringkas (*Abstract Syntax Tree*).

## Rincian Implementasi
Proses abstraksi dikelola oleh komponen `ASTBuilder`, sebuah transformer yang menggunakan pola perancangan perangkat lunak **Visitor Pattern**.

Struktur file yang diterapkan:
- `src/ast_nodes.py`: Menampung representasi kelas logika fungsional murni seperti `Program`, `IfStmt`, `BinaryOp`, dan `Assignment`. Dilengkapi dengan CLI Printer internal `print_ast()`.
- `src/ast_builder.py`: Mesin penelusur pohon yang secara cerdas mendeteksi *root node*, menelusuri ranting-rantingnya, mengeliminasi bagian token tak penting, lalu merakit ulang menjadi kelas node dari `ast_nodes.py`.

## Hasil Validasi (Komparasi Simultan)
Sesuai prosedur ketat kompilator ini, setiap unit test (`tests/test_ast.py`) di Fase 4 wajib memberikan bukti **Double Validation** (Komparasi Visual).
1. Pohon Mentah CST yang berasal dari Fase 3 harus tercetak secara eksplisit bersamaan dengan pohon murni AST dari Fase 4.
2. Hasil uji coba terbukti mampu mengkonversi blok kondisional `kalo_lain` yang semula berisi **30+ token mentah** menjadi representasi kelas biner tunggal, mereduksi hingga lebih dari **60% noise tata bahasa**.
3. *Pass rate* pada unit testing berskala lintas-fase (Fase 2 + Fase 3 + Fase 4) bernilai **100%**.

---
*Terakhir Diperbarui: 2026-06-08*
