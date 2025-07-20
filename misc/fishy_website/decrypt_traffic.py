from typing import List
import base64

# RC4 implementation
def rc4(key: bytes, data: bytes) -> bytes:
    S = list(range(256))
    j = 0

    # Key scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)

    return bytes(out)

# XOR decryption helper (used in decrypt_xor PowerShell function)
def decrypt_xor(encrypted: List[int], xor_key: int) -> str:
    return ''.join(chr(b ^ xor_key) for b in encrypted)

# Global RC4 key (as defined in PowerShell `$global_key`)
global_key = bytes([
    0xf1, 0x6e, 0xcd, 0xc6, 0x79, 0x4c, 0x66, 0xd1, 0x02,
    0xf8, 0x33, 0xc4, 0x86, 0xe7, 0xa4, 0x35, 0x8d, 0x69,
    0xbd, 0xd2, 0x1d, 0x50, 0xf5, 0xfb, 0xdf, 0xec, 0xaf,
    0x0b, 0x9e, 0x53, 0xa4, 0xd3
])

# Example usage
def decrypt_tls_payload(payload: bytes) -> str:
    # Skip TLS record header (first 5 bytes: ContentType + Version + Length)
    encrypted_data = payload[5:]
    decrypted = rc4(global_key, encrypted_data)
    return decrypted.decode("utf-8", errors="ignore")

def decrypt_client_tls_payload(payload: bytes) -> str:
    encrypted_data = payload[5:-4]
    decrypted = rc4(global_key, encrypted_data)
    return decrypted.decode("utf-8", errors="ignore")

stream = open("stream.txt").read().split("\n")
for i in range(len(stream)):
    if i % 2 == 0:
        print(decrypt_tls_payload(bytes.fromhex(stream[i])))
    else:
        print(decrypt_client_tls_payload(bytes.fromhex(stream[i])))

'''
python:
decoded = base64.b64decode("H4sIAAAAAAAAA+3OMQrCQBSE4dSeIieQt3m78QCKlYVorBdZjYVgkeyCQby7iyCIfdTi/5qBaWbOx6GfxmssRiRZbe0zs88UcVoYJ6q1VlJp7mc2V6WMeeol9XHfleU3pv7RYjdvljfjT0md84MkH+zFHzRshnXjm9XWx862rQn3ya+vAgAAAAAAAAAAAAAAAADePAC9uw8vACgAAA==")
with open("keys_backup.tar.gz", "wb") as outfile:
    outfile.write(decoded)


terminal
$ gzip -d keys_backup.tar.gz
$ tar xvf keys_backup.tar
$ cat keys.txt
DUCTF{1_gu355_y0u_c4n_d3cRyPT_TLS_tr4ff1c}
'''