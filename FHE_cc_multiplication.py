import latticebased as lb
import BFV_setup as setup


# ==========================================
# HELPER (Mathematical Helper Functions)
# ==========================================
def poly_mul_integers(a, b, basis):
    """Polynomial multiplication in the Integer domain (Large/Infinite Modulus Q)"""
    n = len(basis) - 1
    res = [0] * (2 * n)
    for i in range(len(a)):
        for j in range(len(b)):
            res[i + j] += a[i] * b[j]
            
    final_res = [0] * n
    for i in range(2 * n):
        val = res[i]
        if i < n: final_res[i] += val
        else:     final_res[i % n] -= val
    return final_res

# ==========================================
# 4 MAIN STEPS (ACCORDING TO SUMMARY D-2.7.5)
# ==========================================

def Step1_ModRaise(c0, c1):
    """
    [Step 1] ModRaise
    Theory: Change the modulus from q (small) to Q (large).
    Practice: In Python, integers automatically expand. Therefore we assume
    this input now lies in a very large integer domain.
    """
    print("\n[1] ModRaise: Moving Ciphertext to Q domain (Large Integers)...")
    # In Python we do not need manual casting because int already supports infinite precision.
    # We return the tuple to be processed in the next step.
    return c0, c1

def Step2_Multiplication(c0_a, c1_a, c0_b, c1_b, basis):
    """
    [Step 2] Multiplication (Tensor Product)
    Compute D0, D1, D2 under modulus Q.
    """
    print("[2] Multiplication: Computing Tensor Product (D0, D1, D2)...")
    
    # D0 = c0 * d0
    D0 = poly_mul_integers(c0_a, c0_b, basis)
    
    # D1 = c0*d1 + c1*d0
    term1 = poly_mul_integers(c0_a, c1_b, basis)
    term2 = poly_mul_integers(c1_a, c0_b, basis)
    D1 = [x + y for x, y in zip(term1, term2)]
    
    # D2 = c1 * d1
    D2 = poly_mul_integers(c1_a, c1_b, basis)
    
    print(f"    -> Result D0 (Raw): {D0[:3]}...")
    return D0, D1, D2

def Step3_Relinearization(D0, D1, D2):
    """
    [Step 3] Relinearization
    Theory: Transform Ciphertext Size 3 (D0, D1, D2) back to Size 2.
    Problem: We need an 'Evaluation Key' (Relinearization Key) for this step.
    Demo Solution: We SKIP this step (Pass-through) and allow
    the ciphertext to remain size 3.
    """
    print("[3] Relinearization: (SKIP - No Evaluation Key)")
    print("    -> Ciphertext is left with 3 elements (c0, c1, c2).")
    return D0, D1, D2

def Step4_Rescaling(D0, D1, D2, q, t):
    """
    [Step 4] Rescaling
    Theory: Bring modulus Q back to q (Divide by Delta).
    Formula: round(val * t / q) mod q
    """
    print("[4] Rescaling: Dividing by Delta and returning to mod q...")
    
    def scale_down(poly):
        res = []
        for val in poly:
            # Operation: Round(val / Delta)
            # Delta = q / t, which is equivalent to val * t / q
            scaled_val = (val * t + (q // 2)) // q
            res.append(scaled_val % q)
        return res

    c0_new = scale_down(D0)
    c1_new = scale_down(D1)
    c2_new = scale_down(D2)
    
    print(f"    -> Final Ciphertext (c0): {c0_new}")
    return c0_new, c1_new, c2_new

# ==========================================
# MAIN WRAPPER FUNCTION
# ==========================================
def BFV_Homomorphic_Multiplication(c0a, c1a, c0b, c1b, basis, q, t):
    """Combine the four steps above"""
    
    # 1. ModRaise
    A_large = Step1_ModRaise(c0a, c1a)
    B_large = Step1_ModRaise(c0b, c1b)
    
    # 2. Multiplication
    # Unpack tuples A_large and B_large
    D0, D1, D2 = Step2_Multiplication(A_large[0], A_large[1], B_large[0], B_large[1], basis)
    
    # 3. Relinearization
    D0_relin, D1_relin, D2_relin = Step3_Relinearization(D0, D1, D2)
    
    # 4. Rescaling
    c0, c1, c2 = Step4_Rescaling(D0_relin, D1_relin, D2_relin, q, t)
    
    return c0, c1, c2

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # Parameter Setup
    N, t = 4, 17
    q = 800000 # Large Q (so implicit ModRaise works correctly)
    w = 9
    basis = [1, 0, 0, 0, 1]
    roots = setup.generate_roots(N, t, w)
    
    # Input Data
    pesan_A = [2, 3, 4, 1]
    pesan_B = [5, 2, 1, 3]
    target = [(a*b)%t for a,b in zip(pesan_A, pesan_B)]
    
    print(f"Input A: {pesan_A}")
    print(f"Input B: {pesan_B}")
    
    # Encoding & Encryption (Preparation)
    poly_A = setup.bfv_encoding_step1(pesan_A, N, t, roots)
    poly_B = setup.bfv_encoding_step1(pesan_B, N, t, roots)
    
    pk_a, pk_b, sk = lb.key_generation(N, q, basis)
    c0_a, c1_a = lb.encryption(pk_a, pk_b, poly_A, N, q, t, basis)
    c0_b, c1_b = lb.encryption(pk_a, pk_b, poly_B, N, q, t, basis)
    
    # --- RUN THE MAIN PROCESS ---
    c0_res, c1_res, c2_res = BFV_Homomorphic_Multiplication(c0_a, c1_a, c0_b, c1_b, basis, q, t)
    
    # Decryption (Using Size 3 Decryptor because Relinearization is SKIPPED)
    # We import the size-3 decryptor from previous code or rewrite it here
    def decryption_size3(c0, c1, c2, s, q, t, basis):
        delta = q // t
        s2 = lb.poly_mod(lb.poly_mul(s, s, q), basis, q)
        term1 = lb.poly_mod(lb.poly_mul(c1, s, q), basis, q)
        term2 = lb.poly_mod(lb.poly_mul(c2, s2, q), basis, q)
        # Formula: c0 - c1*s + c2*s^2
        temp = lb.poly_subs(c0, term1, q)
        m_noisy = lb.poly_add(temp, term2, q)
        return [round(x / delta) % t for x in m_noisy]

    poly_hasil = decryption_size3(c0_res, c1_res, c2_res, sk, q, t, basis)
    hasil_akhir = setup.verify_decoding(poly_hasil, t, roots)
    
    print("\n" + "="*30)
    print(f"RESULT : {hasil_akhir}")
    print(f"TARGET: {target}")
    print("="*30)