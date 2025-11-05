#!/usr/bin/env python3
"""
Quick test of the Rich-based word display method.
"""

from bip39_converter import generate_random_bits, encode_50bits_to_words, get_wordlist
from memorizer import display_words_sequence_rich

def main():
    print("Testing Rich-based word display...")
    print("Generating random words...\n")

    # Generate test words
    bits = generate_random_bits(50)
    wordlist = get_wordlist()
    words = encode_50bits_to_words(bits, wordlist)

    print(f"Words to display: {' '.join(words)}")
    print(f"Binary: {bits}\n")

    input("Press Enter to start the display test...")

    # Test the Rich display
    display_words_sequence_rich(words, delay=0.2)

    print("\n✓ Display test complete!")
    print(f"The words were: {' '.join(words)}")

if __name__ == "__main__":
    main()
