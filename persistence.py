from security import generate_key, encrypt, decrypt

def save(my_gpa, avg, mid, rk, password):
    text = str(my_gpa) + '-' + str(avg) + '-' + str(mid) + '-' + str(rk)
    key = generate_key(password)
    encrypted = encrypt(text, key)
    with open('./record.txt', 'wb+') as f:
        f.write(encrypted)

def read(password):
    try:
        with open('./record.txt', 'rb') as f:
            text = f.readline()
            if text is None:
                return 0.0, 0.0, 0.0, 0.0
            key = generate_key(password)
            decrypted = decrypt(text, key)
            stats = decrypted.split('-')
            return float(stats[0]), float(stats[1]), float(stats[2]), float(stats[3])
    except Exception:
        return 0.0, 0.0, 0.0, 0.0
