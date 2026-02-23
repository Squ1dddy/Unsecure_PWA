import bcrypt

password = input("Enter your password: ")
encoded_pass = password.encode("utf-8")

hashed_pass = bcrypt.hashpw(encoded_pass, bcrypt.gensalt())

print(hashed_pass)

check = input("Re enter password to confirm: ").encode("utf-8")
if bcrypt.checkpw(check, hashed_pass):
    print("MATCH")
else:
    print("NO MATCH")