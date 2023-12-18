from sha import sha1_of_file, sha1_hex

print("Hash of 'hello world':")
print(sha1_hex(b'hello world'))
print()

print("Hash of 'Hello world':")
print(sha1_hex(b'Hello world'))
print()

print("Dokument 1:")
print(sha1_of_file('shattered/shattered-1.pdf'))
print()

print("Dokument 2:")
print(sha1_of_file('shattered/shattered-2.pdf'))
