#!/usr/bin/env python3
"""
Non-interactive test of memorizer core functionality.
"""

from bip39_converter import (
    generate_random_bits,
    encode_50bits_to_words,
    decode_words_to_50bits,
    get_wordlist
)

def test_full_cycle():
    """Test the complete encode-decode cycle."""
    print("Testing memorizer core functionality...")
    print("=" * 60)

    # Generate random bits
    bits = generate_random_bits(50)
    print(f"\n1. Generated 50 random bits:")
    print(f"   {bits}")

    # Encode to words
    wordlist = get_wordlist()
    words = encode_50bits_to_words(bits, wordlist)
    print(f"\n2. Encoded to 5 words:")
    print(f"   {' '.join(words)}")

    # Decode back
    decoded_bits = decode_words_to_50bits(words, wordlist)
    print(f"\n3. Decoded back to bits:")
    print(f"   {decoded_bits}")

    # Verify
    print(f"\n4. Verification:")
    print(f"   Original:  {bits}")
    print(f"   Decoded:   {decoded_bits}")
    print(f"   Match: {bits == decoded_bits}")

    assert bits == decoded_bits, "Bits don't match!"

    print("\n" + "=" * 60)
    print("✓ All tests passed!")

    return True


if __name__ == "__main__":
    test_full_cycle()
