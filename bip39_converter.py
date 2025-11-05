"""
Core conversion logic between binary and BIP39 words.
Uses first 1024 words from BIP39 wordlist for 10-bit encoding.
"""

import random
import bip39


def get_wordlist():
    """Get the first 1024 words from BIP39 wordlist (10-bit encoding)."""
    return bip39.INDEX_TO_WORD_TABLE[:1024]


def bits_to_int(bits):
    """Convert a string of bits to an integer."""
    return int(bits, 2)


def int_to_bits(num, length=10):
    """Convert an integer to a binary string of specified length."""
    return format(num, f'0{length}b')


def bits_to_word(bits, wordlist=None):
    """Convert a 10-bit binary string to a word."""
    if wordlist is None:
        wordlist = get_wordlist()
    index = bits_to_int(bits)
    if index >= len(wordlist):
        raise ValueError(f"Index {index} out of range for wordlist")
    return wordlist[index]


def word_to_bits(word, wordlist=None):
    """Convert a word back to its 10-bit binary representation."""
    if wordlist is None:
        wordlist = get_wordlist()
    try:
        index = wordlist.index(word)
        return int_to_bits(index, 10)
    except ValueError:
        raise ValueError(f"Word '{word}' not found in wordlist")


def generate_random_bits(length=50):
    """Generate a random binary string of specified length."""
    return ''.join(random.choice('01') for _ in range(length))


def encode_50bits_to_words(bits, wordlist=None):
    """Convert 50 bits into 5 words (10 bits each)."""
    if wordlist is None:
        wordlist = get_wordlist()
    if len(bits) != 50:
        raise ValueError("Input must be exactly 50 bits")

    words = []
    for i in range(0, 50, 10):
        chunk = bits[i:i+10]
        word = bits_to_word(chunk, wordlist)
        words.append(word)

    return words


def decode_words_to_50bits(words, wordlist=None):
    """Convert 5 words back to 50 bits."""
    if wordlist is None:
        wordlist = get_wordlist()
    if len(words) != 5:
        raise ValueError("Input must be exactly 5 words")

    bits = ''
    for word in words:
        bits += word_to_bits(word, wordlist)

    return bits
