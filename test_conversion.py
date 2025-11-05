#!/usr/bin/env python3
"""
Test script for converting 10-bit sequences to BIP39 words.
Uses the first 1024 words from BIP39 wordlist (2^10 = 1024).
"""

import random
import bip39

def get_wordlist():
    """Get the BIP39 wordlist (2048 words, we'll use first 1024)."""
    wordlist = bip39.INDEX_TO_WORD_TABLE
    # BIP39 has 2048 words (11-bit), we need 1024 words (10-bit)
    return wordlist[:1024]

def bits_to_int(bits):
    """Convert a string of bits to an integer."""
    return int(bits, 2)

def int_to_bits(num, length=10):
    """Convert an integer to a binary string of specified length."""
    return format(num, f'0{length}b')

def bits_to_word(bits, wordlist):
    """Convert a 10-bit binary string to a word."""
    index = bits_to_int(bits)
    if index >= len(wordlist):
        raise ValueError(f"Index {index} out of range for wordlist")
    return wordlist[index]

def word_to_bits(word, wordlist):
    """Convert a word back to its 10-bit binary representation."""
    try:
        index = wordlist.index(word)
        return int_to_bits(index, 10)
    except ValueError:
        raise ValueError(f"Word '{word}' not found in wordlist")

def generate_random_bits(length=50):
    """Generate a random binary string of specified length."""
    return ''.join(random.choice('01') for _ in range(length))

def encode_50bits_to_words(bits, wordlist):
    """Convert 50 bits into 5 words (10 bits each)."""
    if len(bits) != 50:
        raise ValueError("Input must be exactly 50 bits")

    words = []
    for i in range(0, 50, 10):
        chunk = bits[i:i+10]
        word = bits_to_word(chunk, wordlist)
        words.append(word)

    return words

def decode_words_to_50bits(words, wordlist):
    """Convert 5 words back to 50 bits."""
    if len(words) != 5:
        raise ValueError("Input must be exactly 5 words")

    bits = ''
    for word in words:
        bits += word_to_bits(word, wordlist)

    return bits

def main():
    print("=" * 60)
    print("Fast Memorizer - BIP39 10-bit Word Encoding Test")
    print("=" * 60)

    # Get wordlist
    wordlist = get_wordlist()
    print(f"\nWordlist loaded: {len(wordlist)} words")
    print(f"First 10 words: {', '.join(wordlist[:10])}")
    print(f"Last 10 words: {', '.join(wordlist[-10:])}")

    # Test 1: Convert random 10-bit sequences to words
    print("\n" + "-" * 60)
    print("TEST 1: Converting random 10-bit sequences to words")
    print("-" * 60)

    for i in range(5):
        random_bits = generate_random_bits(10)
        word = bits_to_word(random_bits, wordlist)
        index = bits_to_int(random_bits)
        print(f"{random_bits} (decimal: {index:4d}) → {word}")

    # Test 2: Convert 50 bits to 5 words
    print("\n" + "-" * 60)
    print("TEST 2: Converting 50 bits to 5 words")
    print("-" * 60)

    random_50bits = generate_random_bits(50)
    words = encode_50bits_to_words(random_50bits, wordlist)

    print(f"Original 50 bits: {random_50bits}")
    print(f"\nEncoded as 5 words:")
    for i, word in enumerate(words, 1):
        chunk = random_50bits[(i-1)*10:i*10]
        print(f"  {i}. {chunk} → {word}")

    print(f"\nFull sequence: {' '.join(words)}")

    # Test 3: Decode back to verify
    print("\n" + "-" * 60)
    print("TEST 3: Decoding words back to bits (verification)")
    print("-" * 60)

    decoded_bits = decode_words_to_50bits(words, wordlist)
    print(f"Original bits:  {random_50bits}")
    print(f"Decoded bits:   {decoded_bits}")
    print(f"Match: {random_50bits == decoded_bits}")

    # Test 4: Edge cases
    print("\n" + "-" * 60)
    print("TEST 4: Edge cases (0 and max values)")
    print("-" * 60)

    min_bits = "0000000000"
    max_bits = "1111111111"

    min_word = bits_to_word(min_bits, wordlist)
    max_word = bits_to_word(max_bits, wordlist)

    print(f"{min_bits} (decimal: 0)    → {min_word}")
    print(f"{max_bits} (decimal: 1023) → {max_word}")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
