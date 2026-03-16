import bcrypt
# Hashing password setup
password = input("Enter your password: ")
encoded_pass = password.encode("utf-8")

hashed_pass = bcrypt.hashpw(encoded_pass, bcrypt.gensalt())

print(hashed_pass)

check = input("Re enter password to confirm: ").encode("utf-8")
if bcrypt.checkpw(check, hashed_pass):
    print("MATCH")
else:
    print("NO MATCH")

# FIX REDIRECT ISSUES
ALLOWED_REDIRECTS = ['/dashboard', '/profile', '/home']

if request.method == "GET" and request.args.get("url"):
    url = request.args.get("url", "")
    if url in ALLOWED_REDIRECTS:
        return redirect(url, code=302)
    else:
        return redirect('/home', code=302)