import latticebased as lb

def c_to_p_addition(c0, c1, m2, basis, q, t):
    """
    Ciphertext + Plaintext addition.
    The plaintext m2 is first scaled by Delta = q/t,
    then added to the ciphertext component c0.
    """
    delta = q // t
    scaled_m2 = lb.scalar_mul(m2, delta, q)
    result = lb.poly_mod(lb.poly_add(c0, scaled_m2, q), basis, q)
    return result, c1


def cp_addition(combined_m, N, q, t, basis):
    """
    Verification helper:
    Encrypt the already-combined plaintext polynomial
    and decrypt it again to verify the homomorphic result.
    """
    a, b, s = lb.key_generation(N, q, basis)
    c0, c1 = lb.encryption(a, b, combined_m, N, q, t, basis)
    m_dec = lb.decryption(c0, c1, s, q, t, basis)

    return m_dec


def c_to_p_mul(c0, c1, m2, q, basis):
    """
    Ciphertext × Plaintext multiplication.
    Multiply both ciphertext components with plaintext m2.
    """
    c0_m = lb.poly_mod(lb.poly_mul(c0, m2, q), basis, q)
    c1_m = lb.poly_mod(lb.poly_mul(c1, m2, q), basis, q)
    return c0_m, c1_m


def cp_mul(combined_m, N, q, t, basis):
    """
    Verification helper:
    Encrypt the multiplied plaintext polynomial
    and decrypt it again to compare with homomorphic results.
    """
    a, b, s = lb.key_generation(N, q, basis)
    c0, c1 = lb.encryption(a, b, combined_m, N, q, t, basis)
    m_dec = lb.decryption(c0, c1, s, q, t, basis)

    return m_dec