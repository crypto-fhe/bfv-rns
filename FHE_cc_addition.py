from BFV_setup import * 
from latticebased import *
import random

# BFV / RLWE parameters
N = 4
basis = [1] + [0]*(N-1) + [1]     # x^N + 1
q = 40961

# plaintext modulus from batching
t, w = 17, 2  
roots = generate_roots(N, t, w)

# ================= MESSAGE 1 =================
message1 = [random.randint(0, t-1) for _ in range(N)]
print("Message 1:", message1)

m1_poly = bfv_encoding_step1(message1, N, t, roots)
print("Plaintext poly 1:", m1_poly)

# ================= MESSAGE 2 =================
message2 = [random.randint(0, t-1) for _ in range(N)]
print("\nMessage 2:", message2)

m2_poly = bfv_encoding_step1(message2, N, t, roots)
print("Plaintext poly 2:", m2_poly)

# ================= KEYGEN ==================
a, b, s = key_generation(N, q, basis)

# ================= ENCRYPT =================
c0_1, c1_1 = encryption(a, b, m1_poly, N, q, t, basis)
c0_2, c1_2 = encryption(a, b, m2_poly, N, q, t, basis)

# ================= ADD CIPHERTEXT ==========
c0_sum = poly_add(c0_1, c0_2, q)
c1_sum = poly_add(c1_1, c1_2, q)

# ================= DECRYPT =================
m_sum_dec = decryption(c0_sum, c1_sum, s, q, t, basis)
print("\nDecrypted summed polynomial:", m_sum_dec)

# ================= DECODE ==================
decoded_sum = verify_decoding(m_sum_dec, t, roots)
print("Decoded summed vector:", decoded_sum)

# ================= EXPECTED =================
expected = [(message1[i] + message2[i]) % t for i in range(N)]
print("\nExpected (m1 + m2) mod t:", expected)

print("\nSUCCESS!" if decoded_sum == expected else "\nFAILED!")