# Referensi Bahasa BetawiScript

Dokumen ini berisi daftar lengkap pemetaan (*mapping*) kata kunci (keywords) dan fungsi bawaan (built-in functions) dari bahasa Python ke bahasa BetawiScript.

## 1. Kata Kunci Dasar (Keywords)

### Boolean & Nilai Khusus
* `True` ➔ `Bener`
* `False` ➔ `Kaga`
* `None` ➔ `Kosong`

### Logika
* `and` ➔ `ama`
* `or` ➔ `atawa`
* `not` ➔ `bukan`

### Percabangan
* `if` ➔ `kalo`
* `elif` ➔ `kalo_kaga`
* `else` ➔ `laennya`

### Perulangan
* `for` ➔ `buat`
* `while` ➔ `selagi`
* `in` ➔ `di`
* `break` ➔ `berenti`
* `continue` ➔ `terusin`
* `pass` ➔ `lewat`

### Fungsi
* `def` ➔ `bikin`
* `return` ➔ `balikin`
* `yield` ➔ `hasilin`
* `lambda` ➔ `fungsi_kecil`

### Class / Pemrograman Berorientasi Objek (OOP)
* `class` ➔ `kelas`
* `self` ➔ `gue`
* `super` ➔ `emak`

### Penanganan Error (Exception Handling)
* `try` ➔ `cobain`
* `except` ➔ `kecuali`
* `finally` ➔ `akhirnya`
* `raise` ➔ `angkat`
* `assert` ➔ `pastiin`

### Import & Modul
* `import` ➔ `ambil`
* `from` ➔ `dari`
* `as` ➔ `sebagai`

### Scope / Konteks
* `global` ➔ `seluruhnya`
* `nonlocal` ➔ `bukan_lokal`
* `with` ➔ `pake`

### Asynchronous (Python 3.5+)
* `async` ➔ `barengan`
* `await` ➔ `tungguin`

### Pattern Matching (Python 3.10+)
* `match` ➔ `cocok`
* `case` ➔ `kasus`

### Lainnya
* `del` ➔ `apus`
* `is` ➔ `ialah`

---

## 2. Fungsi Bawaan (Built-in Functions)

### Input / Output
* `print` ➔ `cetak`
* `input` ➔ `nanya`

### Konversi Tipe Data
* `int` ➔ `angka`
* `float` ➔ `desimal`
* `str` ➔ `teks`
* `bool` ➔ `logika`
* `complex` ➔ `komplek`

### Koleksi / Struktur Data
* `list` ➔ `daftar`
* `tuple` ➔ `kumpulan`
* `set` ➔ `himpunan`
* `dict` ➔ `kamus`
* `frozenset` ➔ `himpunan_baku`

### Operasi Angka
* `abs` ➔ `mutlak`
* `round` ➔ `buletin`
* `pow` ➔ `pangkat`
* `divmod` ➔ `bagisisa`
* `sum` ➔ `jumlah`
* `max` ➔ `paling_gede`
* `min` ➔ `paling_kecil`

### Iterasi
* `len` ➔ `panjang`
* `range` ➔ `jarak`
* `enumerate` ➔ `daftarin`
* `zip` ➔ `gabung`
* `iter` ➔ `ulang`
* `next` ➔ `lanjut`
* `aiter` ➔ `ulang_barengan`
* `anext` ➔ `lanjut_barengan`
* `reversed` ➔ `balikin`
* `sorted` ➔ `urutin`

### Pengecekan Logika Tipe / Refleksi
* `all` ➔ `semuanya`
* `any` ➔ `salah_satu`
* `type` ➔ `jenis`
* `isinstance` ➔ `ujikata`
* `issubclass` ➔ `ujisub`
* `id` ➔ `tanda`
* `callable` ➔ `bisa_dipanggil`

### Karakter & Encoding
* `chr` ➔ `huruf`
* `ord` ➔ `urutan`
* `ascii` ➔ `aski`
* `bin` ➔ `biner`
* `oct` ➔ `oktal`
* `hex` ➔ `heksa`

### Utilitas Objek & Atribut
* `getattr` ➔ `ambil_sifat`
* `setattr` ➔ `atur_sifat`
* `hasattr` ➔ `ada_sifat`
* `delattr` ➔ `apus_sifat`

### Namespace & Memori
* `globals` ➔ `globalnya`
* `locals` ➔ `lokalnya`
* `vars` ➔ `variabelnya`
* `dir` ➔ `arah`
* `bytes` ➔ `bait`
* `bytearray` ➔ `susunan_bait`
* `memoryview` ➔ `liat_memori`

### Utilitas Eksekusi & Kelas
* `eval` ➔ `evaluasi`
* `exec` ➔ `jalanin`
* `compile` ➔ `kompilasi`
* `open` ➔ `buka`
* `map` ➔ `petain`
* `filter` ➔ `saring`
* `property` ➔ `properti`
* `staticmethod` ➔ `metode_statis`
* `classmethod` ➔ `metode_kelas`
* `__import__` ➔ `__ambil__`
* `breakpoint` ➔ `titik_renti`
* `format` ➔ `bentuk`
* `repr` ➔ `wakil`
* `hash` ➔ `acak`
* `help` ➔ `tolong`
* `slice` ➔ `potong`
* `object` ➔ `objek`
