from country_list import available_languages
from passlib.hash import sha256_crypt
import datetime



# generate new salt, hash password
hash = sha256_crypt.hash("password")

# verify password
print(type(sha256_crypt.verify("password", hash)))
print(type(hash))



#print(available_languages())

print(datetime.datetime(2015,1,1).weekday())
string_date="2015-01-01"
print(datetime.datetime.strptime(string_date, "%Y-%m-%d").weekday())