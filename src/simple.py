import numpy as np
from itertools import starmap

# np.poly1d([1, 2, 3])
# np.polymul([1, 2, 3], [9, 5, 1])

# constants!
## how many polynomials per?
size = 2
## Modulus (numerical constants)
q = 17
## Modulus (polynomial)
f = np.poly1d([1,0,0,0,1])

# Keys!
## Private key
s = [np.poly1d([-1,-1,1,0]), np.poly1d([-1,0,-1,0])]
## Public key
A = [
        [np.poly1d([6,16,16,11]), np.poly1d([9,4,6,3])],
        [np.poly1d([5,3,10,1]), np.poly1d([6,1,9,15])]
    ]
## error vector
e = [np.poly1d([1,0,0]), np.poly1d([1,-1,0])]

def mod(poly,f,q):
    _, poly = np.polydiv(poly,f)
    return np.poly1d(np.mod(poly,q))

def vecmul(a,b):
    return sum(starmap(np.polymul, zip(a,b)))

def matmul(A,s,e,f,q):
    t = []
    for idx in range(size):
        # the matrix multiplication
        poly = vecmul(A[idx],s)
        # error addition
        poly += e[idx]
        # modulus
        poly = mod(poly,f,q)
        t.append(poly)
    return t

t = matmul(A,s,e,f,q)

#print("\nPrivate key:")
#for val in s:
#    print(val)
#
#print("\nPublic key:")
#print("\tt:")
#print(t)
#print("\tA:")
#for row in A:
#    print(row)


#####################################################
print("\nLet's try encrypting!")

# needed encryption components
## error polynomial vector
e1 = [np.poly1d([1,1,0]), np.poly1d([1,0,0])]
## randomizer poly vector
r = [np.poly1d([-1,1,0,0]), np.poly1d([1,1,0,-1])]
# error polynomial
e2 = np.poly1d([-1,-1,0,0])


## Actual message sending!
message = 11
# get the polynomial of the binary representation
m = np.poly1d([int(b) for b in bin(message)[2:]])

# scale the polynomial!
scale = round(q/2)
m *= scale

print("MESSAGE:")
print(m)

A_T = list(zip(*A))
u = matmul(A_T,r,e1,f,q)
print("u:")
print(u)
#print(vecmul(t,r))
v = mod(vecmul(t,r) + e2 + m,f,q)
print("v:")
print(v)

#####################################################

print("\nLet's try decrypting!")
mn = np.array(mod(np.polysub(v,vecmul(s,u)),f,q))
print(mn)
mb = (abs(scale-mn) <= scale/2).astype(int)
print(mb)

#####################################################

## An Actual Implementation ##

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

def generate_keys(n,k,q,n1):
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
    # the modulus polynomial
    f = [1]+[0]*n+[1]
    print(f)
    # Keys!
    ## Private key
    s = rand_poly_array(n,k,n1)
    ## Public key
    A = [rand_poly_array(n,k,q-1) for _ in range(k)]
    ## error vector
    e = rand_poly_array(n,k,n1)
    t = matmul(A,s,e,f,q)

    return (s,(A,t))

def encrypt(pk,m,n,k,n1,f,q):
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
    u = matmul(A_T,r,e1,f,q)
    v = mod(vecmul(t,r) + e2 + m,f,q)

    return (u,v)

def decrypt(s,ciphertext,f,q):
    (u,v) = ciphertext
    scale = round(q/2)
    mn = np.array(mod(np.polysub(v,vecmul(s,u)),f,q))
    return (abs(scale-mn) <= scale/2).astype(int)

print("-----------------------")
print("Try my own!")
n = 3
k = 2
q = 17
n1 = 2
# def generate_keys(n,k,q,n1):
private, public = generate_keys(n,k,q,n1)
# private = s
# public = (A,t)
m = 11
# def encrypt(pk,m,n,k,n1,f,q):
cipher = encrypt(public,m,n,k,n1,f,q)
# def decrypt(s,ciphertext):
res = decrypt(private,cipher,f,q)
print(res)
