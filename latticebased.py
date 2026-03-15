import random

def poly_add(a, b, q):
    # a and b are polynomials represented as vectors
    # q is a prime modulus
    if len(a) == len(b):
        n = len(a)
    else:
        raise ValueError("degrees are not equal")
    result = [0]*n
    for i in range(n):
        result[i] = (a[i] + b[i]) % q
    return result

def poly_subs(a, b, q):
    # a and b are polynomials represented as vectors
    # q is a prime modulus
    if len(a) == len(b):
        n = len(a)
    else:
        raise ValueError("degrees are not equal")
    result = [0]*n
    for i in range(n):
        result[i] = (a[i] - b[i]) % q
    return result

def poly_mul(a, b, q):
    # a and b are polynomials represented as vectors
    # q is a prime modulus
    n = len(a)
    result = [0]*(2*n - 1)
    for i in range(len(a)):
        for j in range(len(b)):
           result[i + j] = (result[i + j] + a[i] * b[j]) % q
    return result

def poly_mod(poly, basis, q):
    n = len(basis) - 1  # degree
    while len(poly) > n:
        coef = poly.pop()
        poly[len(poly) - n] = (poly[len(poly) - n] - coef) % q
    return poly

def scalar_mul(poly, scalar, q):
    return [(scalar * x) % q for x in poly]

# ======================
# Random polynomials
# ======================

def uniform_poly(n, q):
    return [random.randint(0, q-1) for _ in range(n)]

def gaussian_error_poly(n, sigma=2):
    return [round(random.gauss(0, sigma)) for _ in range(n)]

def small_ternary_poly(n):
    return [random.choice([-1, 0, 1]) for _ in range(n)]

# ======================
# Key Generation
# ======================

def key_generation(n, q, basis):
    a = uniform_poly(n, q)          # public random polynomial
    s = gaussian_error_poly(n)      # secret key
    e = gaussian_error_poly(n)      # error polynomial

    a_s = poly_mod(poly_mul(a, s, q), basis, q)
    b = poly_add(a_s, e, q)

    return a, b, s

# ======================
# Encryption (BFV-style)
# ======================

def encryption(a, b, message, n, q, t, basis):
    delta = q // t

    r  = gaussian_error_poly(n)
    e0 = gaussian_error_poly(n)
    e1 = gaussian_error_poly(n)

    delta_m = scalar_mul(message, delta, q)

    br = poly_mod(poly_mul(b, r, q), basis, q)
    c0 = poly_add(poly_add(br, e0, q), delta_m, q)
    c0 = poly_mod(c0, basis, q)

    ar = poly_mod(poly_mul(a, r, q), basis, q)
    c1 = poly_add(ar, e1, q)
    c1 = poly_mod(c1, basis, q)

    return c0, c1

# ======================
# Decryption
# ======================

def decryption(c0, c1, s, q, t, basis):
    delta = q // t

    sc1 = poly_mod(poly_mul(c1, s, q), basis, q)
    scaled = poly_subs(c0, sc1, q)

    message = [round(x / delta) % t for x in scaled]
    return message

# # ======================
# # Parameters
# # ======================

# basis = [1, 0, 0, 0, 1]   # x^4 + 1
# n = len(basis) - 1
# q = 40961
# t = 5

# message = [0,0,0,0]

# # ======================
# # Run
# # ======================

# public_a, public_b, secret_s = key_generation(n, q, basis)

# c0, c1 = encryption(public_a, public_b, message, n, q, t, basis)
# decrypted = decryption(c0, c1, secret_s, q, t, basis)

# print("Public key (a, b):", (public_a, public_b))
# print("Secret key:", secret_s)
# print("Plaintext:", message)
# print("Ciphertext:", (c0, c1))
# print("Decrypted:", decrypted)