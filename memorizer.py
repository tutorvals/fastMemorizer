#!/usr/bin/env python3
"""
Fast Memorizer - Terminal tool for training 50-bit memorization.

Displays 5 words sequentially (0.2s each), then prompts for recall.
"""

import time
import random
import string
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich.live import Live

from bip39_converter import (
    generate_random_bits,
    encode_50bits_to_words,
    decode_words_to_50bits,
    get_wordlist
)


console = Console()


def generate_random_scramble(length=8):
    """Generate random characters to scramble the display."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def display_words_sequence_rich(words, delay=0.2):
    """
    Display each word in sequence using Rich Live display.
    Each word is shown for 'delay' seconds, replacing the previous one smoothly.
    Uses Rich's Live context for flicker-free updates.
    """
    console.clear()

    # Display static title and instructions
    console.print("\n[bold cyan]MEMORIZATION TEST[/bold cyan]")
    console.print("[dim]Remember the sequence of 5 words...[/dim]\n")

    # Create Live display for the word
    with Live(console=console, refresh_per_second=10, screen=False) as live:
        # Display each word
        for word in words:
            # Create styled text for the word
            word_text = Text(f" {word.upper()} ", style="bold yellow on blue")
            # Center align it
            centered = Align.center(word_text)
            # Update the live display
            live.update(centered)
            # Wait before showing next word
            time.sleep(delay)

        # After last word, show "FINISHED"
        finished_text = Text(" FINISHED ", style="bold green on white")
        centered_finished = Align.center(finished_text)
        live.update(centered_finished)
        time.sleep(0.3)

    console.print()  # Add blank line after


def display_words_sequence(words, delay=0.2):
    """
    Display each word in sequence, replacing the previous one.
    Each word is shown for 'delay' seconds.
    DEPRECATED: Use display_words_sequence_rich() for better rendering.
    """
    console.clear()

    # Display title
    console.print("\n[bold cyan]MEMORIZATION TEST[/bold cyan]")
    console.print("[dim]Remember the sequence of 5 words...[/dim]\n")

    # Display each word in the same location
    for i, word in enumerate(words):
        # Use carriage return to go back to start of line and clear it
        if i > 0:
            # Move cursor up one line and clear it
            console.print("\033[F\033[K", end="")

        # Print the word
        console.print(f"[bold yellow on blue] {word.upper()} [/bold yellow on blue]")
        time.sleep(delay)

    # After last word, replace with "finished"
    console.print("\033[F\033[K", end="")  # Move up and clear line
    console.print("[bold green on white] FINISHED [/bold green on white]")
    time.sleep(0.3)


def get_user_input():
    """Prompt user to input the 5 words they remember."""
    console.print("\n" + "=" * 60)
    console.print("[bold green]Enter the 5 words you remember (separated by spaces):[/bold green]")

    user_input = Prompt.ask("[cyan]Your answer[/cyan]")

    # Parse input
    words = user_input.strip().lower().split()

    return words


def check_answer(correct_words, user_words):
    """
    Compare user's words with correct sequence.
    Returns (is_correct, details)
    """
    if len(user_words) != 5:
        return False, f"Expected 5 words, got {len(user_words)}"

    matches = []
    for i, (correct, user) in enumerate(zip(correct_words, user_words)):
        matches.append(correct == user)

    all_correct = all(matches)

    return all_correct, matches


def display_results(correct_words, user_words, matches, correct_bits):
    """Display the results of the memorization test."""
    console.print("\n" + "=" * 60)
    console.print("[bold]RESULTS[/bold]")
    console.print("=" * 60)

    # Show word-by-word comparison
    for i, (correct, user, match) in enumerate(zip(correct_words, user_words, matches)):
        if match:
            console.print(f"  {i+1}. [green]✓[/green] {correct}")
        else:
            console.print(f"  {i+1}. [red]✗[/red] {correct} (you said: {user})")

    # Show overall result
    console.print()
    if all(matches):
        console.print("[bold green]🎉 PERFECT! All words correct![/bold green]")
        console.print(f"[dim]Binary: {correct_bits}[/dim]")
    else:
        correct_count = sum(matches)
        console.print(f"[yellow]Score: {correct_count}/5 words correct[/yellow]")
        console.print(f"[dim]Correct sequence: {' '.join(correct_words)}[/dim]")
        console.print(f"[dim]Binary: {correct_bits}[/dim]")


def run_memorization_test():
    """Run a complete memorization test cycle."""
    # Generate random 50 bits
    bits = generate_random_bits(50)

    # Convert to words
    wordlist = get_wordlist()
    words = encode_50bits_to_words(bits, wordlist)

    # Display sequence
    console.print("\n[bold]Starting in 3 seconds...[/bold]")
    time.sleep(1)
    console.print("[bold]Get ready...[/bold]")
    time.sleep(1)
    console.print("[bold]GO![/bold]")
    time.sleep(1)

    display_words_sequence_rich(words, delay=0.2)

    # Get user input
    user_words = get_user_input()

    # Check answer
    is_correct, matches = check_answer(words, user_words)

    # Display results
    if len(user_words) != 5:
        console.print(f"\n[red]Error: {matches}[/red]")
        console.print(f"[dim]Correct answer was: {' '.join(words)}[/dim]")
        console.print(f"[dim]Binary: {bits}[/dim]")
    else:
        display_results(words, user_words, matches, bits)

    return is_correct


def main():
    """Main entry point for the memorizer tool."""
    console.clear()

    # Welcome message
    panel = Panel.fit(
        "[bold cyan]Fast Memorizer[/bold cyan]\n\n"
        "Train your brain to memorize 50 bits in 1 second!\n"
        "You'll see 5 words displayed for 0.2 seconds each.\n"
        "Try to remember and recall them all.",
        border_style="cyan"
    )
    console.print(panel)
    console.print()

    # Ask if ready
    ready = Prompt.ask("[yellow]Ready to start?[/yellow]", choices=["y", "n"], default="y")

    if ready.lower() != 'y':
        console.print("[dim]Maybe next time![/dim]")
        return

    # Run test
    run_memorization_test()

    # Ask to continue
    console.print("\n")
    again = Prompt.ask("[yellow]Try again?[/yellow]", choices=["y", "n"], default="y")

    while again.lower() == 'y':
        console.print()
        run_memorization_test()
        console.print("\n")
        again = Prompt.ask("[yellow]Try again?[/yellow]", choices=["y", "n"], default="y")

    console.print("\n[bold green]Thanks for training! Keep practicing! 🧠[/bold green]")


if __name__ == "__main__":
    main()
