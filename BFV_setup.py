# ==========================================
# Search for BFV Parameters for Batch Encoding
# ==========================================

def is_prime(num):
    """Check whether a number is Prime."""
    if num < 2: return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def get_prime_factors(num):
    """Find prime factors of a number (used to check Primitive Root)."""
    i = 2
    factors = set()
    temp = num
    while i * i <= temp:
        if temp % i:
            i += 1
        else:
            temp //= i
            factors.add(i)
    if temp > 1:
        factors.add(temp)
    return factors

def is_primitive_root(g, t):
    """
    Check whether g is a Primitive Root of t.
    Condition: g^((t-1)/factor) mod t != 1 for all prime factors of t-1.
    """
    factors = get_prime_factors(t - 1)
    for factor in factors:
        exponent = (t - 1) // factor
        if pow(g, exponent, t) == 1:
            return False
    return True

def find_bfv_parameters(N):
    print(f"--- SEARCHING PARAMETERS FOR N = {N} ---")
    
    # 1. Find Modulus t (Prime that satisfies t = k * 2N + 1)
    # We search k from 1, 2, 3... until a valid prime is found.
    two_n = 2 * N
    k = 1
    t = 0
    while True:
        candidate_t = (k * two_n) + 1
        if is_prime(candidate_t):
            t = candidate_t
            break
        k += 1
    
    print(f"[1] Modulus (t) found: {t}")
    print(f"    (Obtained from k={k}: {k} * {two_n} + 1 = {t})")

    # 2. Find Primitive Root (g) of t
    # Try numbers from 2, 3, 4... until a valid primitive root is found.
    g = 0
    for candidate_g in range(2, t):
        if is_primitive_root(candidate_g, t):
            g = candidate_g
            break
            
    print(f"[2] Primitive Root (g) of {t} is: {g}")

    # 3. Compute Batching Generator (omega)
    # Formula: omega = g ^ ((t-1) / 2N) mod t
    exponent = (t - 1) // two_n
    omega = pow(g, exponent, t)
    
    print(f"[3] Generator Omega (w) is: {omega}")
    print(f"    (Computed from {g}^{exponent} mod {t})")
    
    # 4. Final Verification (Check Roots of Unity)
    print("\n--- ROOTS VERIFICATION ---")
    roots = []
    for i in range(N):
        val = pow(omega, 2*i + 1, t)
        roots.append(val)
    print(f"Roots of Unity (Slot Positions): {roots}")
    
    return t, g, omega

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def generate_roots(n, modulus, w):
    """Generate an array of Roots of Unity (Slot Positions)."""
    roots = []
    for i in range(n):
        # Formula: w^(2i + 1) mod t
        val = pow(w, 2*i + 1, modulus)
        roots.append(val)
    return roots

# ==========================================
# CORE 1: ENCODING (Vector -> Polynomial)
# ==========================================
def bfv_encoding_step1(v, n, modulus, roots):
    print(f"\n--- START ENCODING ---")
    print(f"Input Vector (v): {v}")

    # STEP 1: Reversal (I_n^R)
    # Reverse the input vector order
    v_reversed = v[::-1]
    print(f"[1] Reversal (v_rev): {v_reversed}")

    # STEP 2 & 3: Matrix Multiplication W + Scaling
    # Formula: m = n^-1 * W * v_rev
    
    # First compute modular inverse of N (n^-1 mod t)
    # Python 3.8+ allows pow(a, -1, m)
    inv_n = pow(n, -1, modulus) 
    print(f"[2] Scaling Factor (n^-1): {inv_n}")

    koefisien_m = []

    # Loop over Matrix Rows (i = 0 to N-1)
    for i in range(n):
        row_sum = 0
        
        # Loop over Matrix Columns (j = 0 to N-1)
        for j in range(n):
            # Compute matrix element W[i][j] = (root_j)^i
            # where root_j is roots[j]
            w_element = pow(roots[j], i, modulus)
            
            # Multiply with the reversed vector element
            term = (w_element * v_reversed[j])
            row_sum += term
            
        # Apply modulo t to the row summation
        row_sum = row_sum % modulus
        
        # FINAL STEP: Multiply by inv_n (Scaling)
        final_val = (row_sum * inv_n) % modulus
        koefisien_m.append(final_val)

    return koefisien_m

# ==========================================
# CORE 2: DECODING (Verification)
# ==========================================
def verify_decoding(poly_coeffs, modulus, roots):
    """
    Convert the polynomial back into the message.
    Method: Evaluate the polynomial at the Roots points.
    """
    print(f"\n--- VERIFICATION (DECODING) ---")
    decoded_msg = []
    
    for i, x in enumerate(roots):
        # Evaluate P(x) = a0 + a1*x + a2*x^2 + ...
        val = 0
        for exponent, coef in enumerate(poly_coeffs):
            term = (coef * pow(x, exponent, modulus))
            val = (val + term)
        
        val = val % modulus
        decoded_msg.append(val)
        print(f"Slot {i} (root={x}) -> Result: {val}")
        
    return decoded_msg