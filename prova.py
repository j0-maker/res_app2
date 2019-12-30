from passlib.hash import sha256_crypt

# generate new salt, hash password
hash = sha256_crypt.hash("password")

# verify password
print(type(sha256_crypt.verify("password", hash)))
print(type(hash))
