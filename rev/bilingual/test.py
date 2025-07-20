import string

charset = string.ascii_letters + string.digits
MOD = 2**32
def rc4(key: bytes, data: list):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for n in range(len(data)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        data[n] ^= S[(S[i] + S[j]) % 256]

    return data

def get_hash(s, target):
	cur = 0x1505
	for c in s:
		cur = cur * 0x21 ^ c
		cur %= MOD 

	# print(hex(cur))
	return cur == target


# s = [0xf2, 0x1e, 0x2a, 0xf4, 0x21, 0xef, 0xf7, 0x29, 0x1b, 0x8b, 0x96, 0x17, 0x78, 0x8b, 0x32, 0x90, 0x87, 0xb4, 0x58, 0xb5, 0xe1, 0xed, 0xb9, 0x48, 0x3e, 0xd9]

nums_raw = [0x5ac1e9d0, 0x31280c9e, 0x685d2458, 0xe76f8d54, 0xe5d7dbf6, 0x46284bc0, 0xcd7ea4e7, 0x41f4f807]
s = []
for num in nums_raw:
	num_bytes = int.to_bytes(num, 4, "little")
	for b in num_bytes:
		s.append(b)

# print(bytes(s).hex())
PASSWORD = "Hydr0ph11de3"

key = [0x7a, 0x6d, 0, 0x59, 0x79, 0x64, 0x7f, 0]
key[4] = ord(PASSWORD[1])
key[5] = ord(PASSWORD[2])
key[6] = ord(PASSWORD[3]) ^ ord(PASSWORD[1]) ^ ord(PASSWORD[2]) ^ 0x10

for val1 in range(256):
	key[2] = val1
	for val2 in range(256):
		key[7] = val2
		print(val1, val2)
		
		new_s = [val for val in s]
		rc4(key, new_s)
		if get_hash(new_s, 0x69fa99d):
			print("Correct!")
			print(key)
			exit(1)

exit()

rc4(b"\x7a\x6d", s)
print("".join(map(chr, s[::2])))
print(s)
if get_hash(s, 0x6293def8):
	print("Correct!")