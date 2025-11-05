# Fast Memorizer

A tool to temporarily memorize 50 bits of information in one second using human reading ability and word translation.

## Concept

- 10 bits = 1 word (1024 possible words)
- 50 bits = 5 words
- Read sequence → Remember → Retranscribe → Convert back to binary

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Run the Memorization Trainer

Train your brain to memorize 50 bits (5 words) in 1 second:

```bash
source venv/bin/activate
python memorizer.py
```

The tool will:
1. Display 5 words sequentially (0.2 seconds each)
2. Show random characters to clear the last word from view
3. Prompt you to recall and type the 5 words
4. Verify your answer and show results

### Test Core Conversion Logic

```bash
python test_conversion.py
```

### Test Memorizer Core Functionality

```bash
python test_memorizer.py
```

## Files

- `bip39_converter.py` - Core conversion logic (binary ↔ words)
- `memorizer.py` - Interactive terminal training tool
- `test_conversion.py` - Test suite for conversion logic
- `test_memorizer.py` - Non-interactive functionality test
