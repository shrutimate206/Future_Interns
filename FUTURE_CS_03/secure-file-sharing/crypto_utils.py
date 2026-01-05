from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY_FILE = "secret.key"

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_file(data):
    key = load_key()
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + encrypted

def decrypt_file(data):
    key = load_key()
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data[16:]), AES.block_size)


