def bit_length(data: bytearray):
    return len(data) * 8


def chunks(data: bytearray, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def u32_words(data: bytearray):
    return [int.from_bytes(data[i:i + 4], byteorder='big') for i in range(0, len(data), 4)]


def extend_to_size(w, length):
    w.extend([0] * (length - len(w)))


def left_shift(num, n):
    return ((num << n) | (num >> (32 - n))) & 0xFFFFFFFF


def one_round(a, b, c, d, e, K, f, w):
    a_ = (left_shift(a, 5) + f + e + K + w) % (2 ** 32)
    b_ = a
    c_ = left_shift(b, 30)
    d_ = c
    e_ = d
    return a_, b_, c_, d_, e_


def padding(length):
    k = (56 - 1 - (length // 8)) % 64  # 448 / 8 and 512 / 8
    zeros = [0] * k
    return bytearray([
        0b10000000,
        *zeros,
        *length.to_bytes(8, byteorder='big')
    ])


def concat(*values):
    result = bytearray()
    for v in values:
        result.extend(v.to_bytes(4, byteorder='big'))
    return result


def sha1(value: bytes):
    data = bytearray(value)

    # append padding
    N = bit_length(data)
    P = padding(N)
    data.extend(P)

    # initial hash value
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    # split into 512 bit blocks
    for chunk in chunks(data, 64):

        # assign input to w(t)
        w = u32_words(chunk)
        extend_to_size(w, 80)

        # calculate w(t) by previous values
        for t in range(16, 80):
            w[t] = left_shift(w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16], 1)

        # init temporary a, b, c, d, e
        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]

        # first 20 rounds
        for t in range(0, 20):
            f = (b & c) | (~b & d)
            K = 0x5A827999
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t])

        # second 20 rounds
        for t in range(20, 40):
            f = b ^ c ^ d
            K = 0x6ED9EBA1
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t])

        # third 20 rounds
        for t in range(40, 60):
            f = (b & c) | (b & d) | (c & d)
            K = 0x8F1BBCDC
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t])

        # fourth 20 rounds
        for t in range(60, 80):
            f = b ^ c ^ d
            K = 0xCA62C1D6
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t])

        # adding the output with the hash value
        h[0] = (h[0] + a) % (2**32)
        h[1] = (h[1] + b) % (2**32)
        h[2] = (h[2] + c) % (2**32)
        h[3] = (h[3] + d) % (2**32)
        h[4] = (h[4] + e) % (2**32)

    return concat(h[0], h[1], h[2], h[3], h[4])
