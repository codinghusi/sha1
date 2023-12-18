from sha.sha1 import bit_length, u32_words, chunks, left_shift


def to_hex(values):
    return ''.join(f'{x:02x}' for x in values).upper()


def to_hex4(x):
    return f'{x:02x}'.upper()


def one_round(a, b, c, d, e, K, f, w, t):
    if t % 20 < 2 or t == 78 or t == 79:
        print(f"t = {t}")
        print(f"\tA' = (A << 5) + f_t + E + K_t + w_t mod 2^32"
              f"\n\t\t= ({to_hex4(a)} << 5) + {to_hex4(f)} + {to_hex4(e)} + {to_hex4(K)} + {to_hex4(w)} mod 2^32"
              f"\n\t\t= ({left_shift(a, 5)}) + {to_hex4(f)} + {to_hex4(e)} + {to_hex4(K)} + {to_hex4(w)} mod 2^32"
              f"\n\t\t= {to_hex4((left_shift(a, 5) + f + e + K + w) % (2 ** 32))}")
        print(f"\tB' = A = {to_hex4(a)}")
        print(f"\tC' = B << 30 = {to_hex4(b)} << 30 = {to_hex4(left_shift(b, 30))}")
        print(f"\tD' = C = {to_hex4(c)}")
        print(f"\tE' = D = {to_hex4(d)}")
    return (
        (left_shift(a, 5) + f + e + K + w) % (2 ** 32),
        a,
        left_shift(b, 30),
        c,
        d
    )


def sha1_vis(value: bytes):
    data = bytearray(value)

    print(f"sha1( {to_hex(data)} )")
    print()

    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    message_length = bit_length(data)

    print(f"l = {message_length} bits")

    # PADDING
    # append 1
    data.append(0b10000000)

    # append 0..0 until number of bits % 512 = 448
    padding = (56 - len(data)) % 64  # 448 / 8 and 512 / 8
    data.extend(bytearray([0 for _ in range(padding)]))

    # append message_length as 64bit
    data.extend(message_length.to_bytes(8, byteorder='big'))

    print(f"k = {padding * 8 + 7} zeros")
    print(f"P = {padding * 8 + 8 + 64} bits")
    # print(f"""Padding is {to_hex(bytearray([
    #     0b10000000,
    #     *([0] * padding),
    #     message_length.to_bytes(8, byteorder='big')
    # ]))}""")

    print(f"""Padding is {to_hex(bytearray([1<<7, *([0]*padding), *list(message_length.to_bytes(8, byteorder='big'))]))}""")
    print()

    print(f"Gesamt M = {to_hex(data)}")
    print()

    print(f"H_0 = {to_hex4(h[0])}, H_1 = {to_hex4(h[1])}, H_2 = {to_hex4(h[2])}, H_3 = {to_hex4(h[3])}, H_4 = {to_hex4(h[4])}")
    print()

    # into 512 bit blocks
    i = 0
    for chunk in chunks(data, 64):
        print(f"## Block {i}")
        i += 1

        w = u32_words(chunk)
        w.extend([0 for _ in range(16, 80)])
        for t in range(16, 80):
            w[t] = left_shift(w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16], 1)
            if t < 20:
                print(f"w_{t} = (w_{t-3} ^ w{t-8} ^ w_{t-14} ^ w_{t-16}) << 1 = ({to_hex4(w[t-3])} ^ {to_hex4(w[t-8])} ^ {to_hex4(w[t-14])} ^ {to_hex4(w[t-16])}) << 1 = {to_hex4(w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16])} << 1 = {to_hex4(w[t])}")

        print("...")
        print()

        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]

        print(f"A = {to_hex4(a)}"
              f"\nB = {to_hex4(b)}"
              f"\nC = {to_hex4(c)}"
              f"\nD = {to_hex4(d)}"
              f"\nE = {to_hex4(e)}")
        print()

        print("0 <= t < 20:")
        print("f_t = (b & c) | (~b & d)")
        print("K_t = 5A827999")
        for t in range(0, 20):
            f = (b & c) | (~b & d)
            K = 0x5A827999
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t], t)
        print()

        print("20 <= t < 40:")
        print("f_t = b ^ c ^ d")
        print("K_t = 6ED9EBA1")
        for t in range(20, 40):
            f = b ^ c ^ d
            K = 0x6ED9EBA1
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t], t)
        print()

        print("40 <= t < 60:")
        print("f_t = (b & c) | (b & d) | (c & d)")
        print("K_t = 8F1BBCDC")
        for t in range(40, 60):
            f = (b & c) | (b & d) | (c & d)
            K = 0x8F1BBCDC
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t], t)
        print()

        print("60 <= t < 80:")
        print("f_t = b ^ c ^ d")
        print("K_t = CA62C1D6")
        for t in range(60, 80):
            f = b ^ c ^ d
            K = 0xCA62C1D6
            a, b, c, d, e = one_round(a, b, c, d, e, K, f, w[t], t)
        print()

        print(f"H_0 = H_0 + A mod 2^32= {to_hex4(h[0])} + {to_hex4(a)} mod 2^32 = {to_hex4((h[0] + a) % (2**32))}")
        print(f"H_1 = H_1 + B mod 2^32= {to_hex4(h[1])} + {to_hex4(b)} mod 2^32 = {to_hex4((h[1] + b) % (2**32))}")
        print(f"H_2 = H_2 + C mod 2^32= {to_hex4(h[2])} + {to_hex4(c)} mod 2^32 = {to_hex4((h[2] + c) % (2**32))}")
        print(f"H_3 = H_3 + D mod 2^32= {to_hex4(h[3])} + {to_hex4(d)} mod 2^32 = {to_hex4((h[3] + d) % (2**32))}")
        print(f"H_4 = H_4 + E mod 2^32= {to_hex4(h[4])} + {to_hex4(e)} mod 2^32 = {to_hex4((h[4] + e) % (2**32))}")
        h[0] = (h[0] + a) % (2**32)
        h[1] = (h[1] + b) % (2**32)
        h[2] = (h[2] + c) % (2**32)
        h[3] = (h[3] + d) % (2**32)
        h[4] = (h[4] + e) % (2**32)

    result = bytearray(h[0].to_bytes(4, byteorder='big'))
    result.extend(h[1].to_bytes(4, byteorder='big'))
    result.extend(h[2].to_bytes(4, byteorder='big'))
    result.extend(h[3].to_bytes(4, byteorder='big'))
    result.extend(h[4].to_bytes(4, byteorder='big'))