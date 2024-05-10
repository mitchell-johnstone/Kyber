mkdir -p files
pushd files
for ((i = 0; i<$1; i++))
do
    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048 >/dev/null 2>&1
    openssl rsa -pubout -in private_key.pem -out public_key.pem >/dev/null 2>&1
    openssl rand 32 > random_key.bin
    openssl rsautl -encrypt -inkey public_key.pem -pubin -in random_key.bin -out encapsulated_key.bin >/dev/null 2>&1
    openssl rsautl -decrypt -inkey private_key.pem -in encapsulated_key.bin -out decrypted_key.bin >/dev/null 2>&1
    rm *
done
#openssl rsa -in private_key.pem -text -noout
popd
rmdir files
