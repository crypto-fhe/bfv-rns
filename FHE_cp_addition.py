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

message1 = [random.randint(1,t-1) for _ in range(N)]
message2 = [random.randint(1,t-1) for _ in range(N)]
added = [(message1[i] + message2[i]) % t for i in range(N)]

# ================= Encoding =================
m_poly_added = bfv_encoding_step1(added, N, t, roots)

m_poly1 = bfv_encoding_step1(message1, N, t, roots)
m_poly2 = bfv_encoding_step1(message2, N, t, roots)

# ================= KeyGen ====================
a, b, s = key_generation(N, q, basis)

# ================= Encryption ================
c0, c1 = encryption(a, b, m_poly1, N, q, t, basis)

# ================= Homomorphic C + P =========
c0_added, c1_added = hmop.c_to_p_addition(
    c0, c1, m_poly2, basis, q, t
)

m_dec_poly = hmop.cp_addition(m_poly_added, N, q, t, basis)

# ================= Decryption ================
m_dec_poly1 = decryption(c0_added, c1_added, s, q, t, basis)

# ================= Decoding ==================
decoded_message = verify_decoding(m_dec_poly, t, roots)
decoded_message2 = verify_decoding(m_dec_poly1, t, roots)

print("Decoded vector addition directly:", decoded_message)
print("Decoded vector addition after encryption:", decoded_message2)

# ================= Expected ==================
expected = [(message1[i] + message2[i]) % t for i in range(N)]
print("Expected added:", expected)