from kyber import *

# def generate_keys(n,k,q,n1):
private, public = generate_keys()

#m = 11
message = "hello world"
print(message)
m = ""
for c in message:
    #print(ord(c),"->",format(ord(c), '08b'))
    m += format(ord(c), '08b')
print(m)
m = int(m,2)

# def encrypt(pk,m,n,k,n1,f,q):
cipher = encrypt(public,m)

# def decrypt(s,ciphertext):
res = decrypt(private,cipher)
for i in res:
    print(i,end="")
print()
res = res.reshape((-1,8))
bc = np.array([2**(7-i) for i in range(8)])
res = res@bc
res = res[res!=0]
print(res)
print("".join([chr(item) for item in res]))
# actual: 1011011001100100
# was:    1011011001100100
#m = ""
#for i in range(len(res)//8):
#    b = "".join(list(map(str,res[i:i+8])))
#    print(b,end="")
#    m += chr(int(b,2))
#print(m)

