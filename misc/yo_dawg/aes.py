from Crypto.Cipher import AES
import base64

KEY = b"qwertyuiopasdfghjklzxcvbnmNOSURF"
IV = b"0123456789DUCTF!"

def decrypt(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(ciphertext).decode("UTF-8")

ct = input("Enter base64: ")
print(decrypt(KEY, IV, base64.b64decode(ct)))