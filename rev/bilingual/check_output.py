with open("output.txt", "r") as infile:
    contents = infile.read().split("\n")[1::2]

print(set(contents), len(set(contents)))