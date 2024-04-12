import numpy as np
from itertools import starmap

n = 3
k = 2
q = 17
n1 = 2

n,k,q,n1 = 256, 2, 3329, 3
# the modulus polynomial
f = [1]+[0]*n+[1]

def mod(poly):
    _, poly = np.polydiv(poly,f)
    return np.poly1d(np.mod(poly,q))

def vecmul(a,b):
    return sum(starmap(np.polymul, zip(a,b)))

def matmul(A,s,e):
    t = []
    for idx in range(k):
        # the matrix multiplication
        poly = vecmul(A[idx],s)
        # error addition
        poly += e[idx]
        # modulus
        poly = mod(poly)
        t.append(poly)
    return t

rng = np.random.default_rng()
def rand_poly(n,n1):
    """
    generate a random polynomial
    """
    return np.poly1d(rng.integers(low=0, high=n1, size=n+1))

def rand_poly_array(n,k,n1):
    """
    generate a random array of polynomials
    """
    return [rand_poly(n,n1) for _ in range(k)]

def generate_keys():
    """
    generate the public / private keys of the Kyber algorithm.
    inputs:
        n: maximum degree of the used polynomials
        k: number of polynomials per vector
        q: modulus for numbers
        n1: control how big coefficients of “small” polynomials can be
    output:
        tuple
            private key
            public key
    """
    # Keys!
    ## Private key
    s = rand_poly_array(n,k,n1)
    ## Public key
    A = [rand_poly_array(n,k,q-1) for _ in range(k)]
    ## error vector
    e = rand_poly_array(n,k,n1)
    t = matmul(A,s,e)

    return (s,(A,t))

def encrypt(pk, message):
    """
    encrypt a single number
    """
    # unpack the public key
    A,t = pk
    # error polynomial
    e1 = rand_poly_array(n,k,n1)
    ## randomizer poly vector
    r = rand_poly_array(n,k,n1)
    # error polynomial
    e2 = rand_poly(n,n1)

    # get the polynomial of the binary representation
    m = np.poly1d(list(map(int,bin(message)[2:])))

    # scale the polynomial!
    scale = round(q/2)
    m *= scale

    A_T = list(zip(*A))
    u = matmul(A_T,r,e1)
    v = mod(vecmul(t,r) + e2 + m)

    return (u,v)

def decrypt(s,ciphertext):
    (u,v) = ciphertext
    scale = round(q/2)
    mn = np.array(mod(np.polysub(v,vecmul(s,u))))
    return (abs(scale-mn) <= scale/2).astype(int)[-n:]
