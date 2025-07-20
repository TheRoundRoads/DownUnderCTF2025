from Crypto.Cipher import DES
import base64
def pad(text):
    n = len(text) % 8
    return text + (b' ' * n)

key = b'hack' + b"\x00" * 4
text1 = 'UDR6b0hwIOkbJ90U/dYB3iSF5iQ50Ci1b+T+YCQPJA3pl9IFtyJFrCWfB1szPlKy5EdvDb029rZ7w2gUAcSJiQ=='
ct = base64.b64decode(text1)

des = DES.new(key, DES.MODE_CBC)

plaintext = des.decrypt(ct)

print(plaintext)