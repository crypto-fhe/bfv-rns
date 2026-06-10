# BFV Homomorphic Encryption – Implementasi Python

Repositori ini berisi implementasi Python dari skema **Fully Homomorphic Encryption (FHE)** tipe **BFV (Brakerski-Fan-Vercauteren)**, dengan dukungan untuk operasi homomorphic seperti penjumlahan, perkalian, dan operasi ciphertext–plaintext untuk efisiensi komputasi.

Kode ini mengacu pada materi dari buku referensi:

> 📖 *Homomorphic Encryption – From Basic Math to Advanced Techniques*  
> (sumber yang disediakan dalam diskusi)

---

## Struktur Repositori

| File | Deskripsi |
|------|-----------|
| `BFV_setup.py` | Parameter dasar BFV (N, t, q, Δ), pembangkitan kunci, encoding/decoding vektor pesan. |
| `latticebased.py` | Implementasi dasar LWE, RLWE, GLWE sebagai fondasi kriptografi lattice. |
| `FHE_cp_addition.py` | Homomorphic ciphertext–plaintext addition (tambah ciphertext dengan plaintext). |
| `FHE_cc_addition.py` | Homomorphic ciphertext–ciphertext addition (tambah ciphertext dengan ciphertext). |
| `FHE_cp_multiplication.py` | Homomorphic ciphertext–plaintext multiplication (kali ciphertext dengan plaintext). |
| `FHE_cc_multiplication.py` | Homomorphic ciphertext–ciphertext multiplication (perkalian dua ciphertext). |
| `Homomorphic_cp_Op.py` | Operasi batch gabungan antara ciphertext dan plaintext (untuk SIMD). |
| `fast_Bconvex.py` | Implementasi Fast Base Conversion (FastBConv), SmallMont, FastBConvEx untuk RNS. |

---

## Fitur Utama

- Encoding/decoding vektor pesan ke dalam polinomial (INTT)
- Enkripsi/dekripsi RLWE dengan scaling factor Δ = ⌊q/t⌋
- Batch encoding (SIMD) untuk vektor ukuran n
- Homomorphic addition (ciphertext–ciphertext)
- Homomorphic addition (ciphertext–plaintext)
- Homomorphic multiplication (ciphertext–plaintext)
- Relinearization menggunakan RLev key
- Modulus switching (ModRaise, ModSwitch)
---

## Skema Kriptografi yang Digunakan

| Komponen | Detail |
|----------|--------|
| Skema utama | BFV (Brakerski–Fan–Vercauteren) |
| Hard problem | RLWE (Ring Learning with Errors) |
| Ring polinomial | ℤ_q[x]/(xⁿ + 1), n = power of two |
| Plaintext modulus | t (prima atau pᵣ) |
| Ciphertext modulus | q (bisa dengan level untuk RNS) |
| Scaling factor | Δ = ⌊q/t⌋ |
| Batch encoding | Evaluasi pada akar-akar Xⁿ + 1 |
| Rotasi slot | Menggunakan helper J(h) = 5ʰ mod 2n |

---

## Referensi Utama

Buku yang menjadi acuan utama pengembangan kode ini:

> **Homomorphic Encryption – From Basic Math to Advanced Techniques**  
> Bagian yang paling relevan:
> - **§D-2**: BFV Scheme (encoding, enkripsi, relinearization, rescaling)
> - **§D-5**: RNS‑variant FHE Schemes (FastBConv, SmallMont, FastBConvEx)
> - **§C-4**: Modulus Switching
> - **§A-10.6**: Isomorphism antara polinomial dan vektor

---

## Cara Menjalankan

### 1. Clone repositori

```bash
git clone https://github.com/username/bfv-homomorphic-encryption.git
cd bfv-homomorphic-encryption
```

### 2. Jalankan contoh

```bash
python BFV_setup.py
python FHE_cc_multiplication.py
python fast_Bconvex.py
```

### 3. Contoh output yang diharapkan

```bash
=== ENCODING dengan FastBConvEx ===
Input vector: [1, 2, 3, 4]
Source moduli: [17, 97]
Target moduli: [7, 11, 13]
...
VERIFIKASI
Original: [1, 2, 3, 4]
Decoded:  [1, 2, 3, 4]
✓ SUCCESS!
```

### Keterbatasan

1. Implementasi ini bersifat edukasional, belum dioptimalkan untuk produksi.
2. Operasi ciphertext–ciphertext multiplication masih dalam tahap pengembangan penuh (utamanya relinearization dan rescaling).
3. Parameter keamanan (n, q, distribusi noise) masih menggunakan nilai kecil agar mudah dipahami.

