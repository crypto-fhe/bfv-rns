import Homomorphic_cp_Operation as hmop
from BFV_setup import * 
from latticebased import *
import random


# ================= Parameters =================
N = 4
basis = [1] + [0]*(N-1) + [1]   # x^N + 1
q = 40961
t, w = 17, 2

roots = generate_roots(N, t, w)

message1 = [random.randint(1, t-1) for _ in range(N)]
message2 = [random.randint(1, t-1) for _ in range(N)]
multiplied = [(message1[i] * message2[i]) % t for i in range(N)]

# ================= Encoding =================
m_poly_multiplied = bfv_encoding_step1(multiplied, N, t, roots)

m_poly1 = bfv_encoding_step1(message1, N, t, roots)
m_poly2 = bfv_encoding_step1(message2, N, t, roots)

# ================= KeyGen ====================
a, b, s = key_generation(N, q, basis)

# ================= Encryption ================
c0, c1 = encryption(a, b, m_poly1, N, q, t, basis)

# ================= Homomorphic C + P =========
c0_multiplied, c1_multiplied = hmop.c_to_p_mul(
    c0, c1, m_poly2, q, basis
)

m_dec_poly = hmop.cp_mul(m_poly_multiplied, N, q, t, basis)

# ================= Decryption ================
m_dec_poly1 = decryption(c0_multiplied, c1_multiplied, s, q, t, basis)

# ================= Decoding ==================
decoded_message = verify_decoding(m_dec_poly, t, roots)
decoded_message2 = verify_decoding(m_dec_poly1, t, roots)

print("Decoded vector multiplication directly:", decoded_message)
print("Decoded vector multiplication after encryption:", decoded_message2)

# ================= Expected ==================
expected = [(message1[i] * message2[i]) % t for i in range(N)]
print("Expected multiplied:", expected)