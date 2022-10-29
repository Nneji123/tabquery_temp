import bcrypt


def hash_password(password: str) -> str:
    if password is not None:
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(str(password).encode("utf-8"), salt)
            return hashed.decode("utf-8")
        except Exception as e:
            print(e)
    else:
        return "Invalid Password entered"


print(hash_password(b"linda321"))
