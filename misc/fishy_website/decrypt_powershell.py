import base64
contents = open("./powershell.txt", "r").read()

# from wide string
decoded = base64.b64decode(contents)
result = "".join(map(chr, [decoded[i] for i in range(0, len(decoded), 2)]))

with open("decoded.ps1", "w") as outfile:
	outfile.write(result)