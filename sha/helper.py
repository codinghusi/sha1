from sha import sha1


def to_hex(values):
    return ''.join(f'{x:02x}' for x in values)


def sha1_hex(data):
    return to_hex(sha1(data))


def sha1_of_file(filename):
    with open(filename, 'rb') as f:
        return sha1_hex(f.read())
