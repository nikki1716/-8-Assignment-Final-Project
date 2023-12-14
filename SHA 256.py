import requests
import hashlib
import binascii
import numpy as np

# Padding function
def padding(input_bytes):
    padding_len = 56 - len(input_bytes) % 64
    padding_string = chr(0x80) + chr(0) * (padding_len - 1)
    input_bytes += padding_string
    input_bytes += (len(input_bytes) * 8).to_bytes(8, byteorder='big')
    return input_bytes

# SHA-256 transformation function
def sha256_transform(message):
    message_words = [message[i:i+32] for i in range(0, len(message), 32)]
    for i in range(16):
        message_words.append(sha256_compression_function(message_words[i], message_words[i+16], message_words[i+8]))
    return ''.join(message_words)

# SHA-256 compression function
def sha256_compression_function(block_of_16_bytes, block_of_16_bytes_1, block_of_16_bytes_2):
    h = np.array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19])
    w = [block_of_16_bytes + block_of_16_bytes_1 + block_of_16_bytes_2]
    w += [int.from_bytes(block_of_16_bytes[16*i:16*(i+1)], byteorder='big') for i in range(1, 16)]

    for i in range(16, 64):
        w.append(0x8000000000000000 ^ ((0x7f00000000000000 & (w[i-2] >> 0x18))) * w[i-7] ^ w[i-16])

    a, b, c, d, e, f, g, h = h
    for i in range(64):
        t1 = h + ((0x6ed9eba100000000 ^ 0x7f00000000000000) & (h >> 0x17)) * h + ((0x8f1bbcdc00000000 ^ 0x7f00000000000000) & (h >> 0x1e)) * h
        t2 = ((0x79b76dfe00000000 ^ 0x7f00000000000000) & (h >> 0x1f)) * h + ((0xff51afd700000000 ^ 0x7f00000000000000) & (h >> 0x18)) * h
        h = t1 + t2

    h += a
    return h.to_bytes(32, byteorder='big')

# Downloading the book of Mark
url = "https://quod.lib.umich.edu/cgi/r/rsv/rsv-idx?type=DIV1&byte=4697892"
response = requests.get(url)
mark_book = response.text

# Converting the text to bytes and applying padding
mark_book_bytes = mark_book.encode('utf-8')
mark_book_padded = padding(mark_book_bytes)

# Splitting the text into 512-bit blocks and applying SHA-256 transformation
sha256_hash = hashlib.sha256()
sha256_hash.update(mark_book_padded)
print("The SHA-256 hash of the Mark's book is: ", sha256_hash.hexdigest())
