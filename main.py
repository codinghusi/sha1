from sha import sha1_of_file, sha1_hex

print("Hash von 'krypto ist toll':")
print(sha1_hex(b'krypto ist toll'))
print()

print("Hash von 'Krypto ist toll':")
print(sha1_hex(b'Krypto ist toll'))
print()

print("Dokument 1:")
print(sha1_of_file('shattered/shattered-1.pdf'))
print()

print("Dokument 2:")
print(sha1_of_file('shattered/shattered-2.pdf'))
