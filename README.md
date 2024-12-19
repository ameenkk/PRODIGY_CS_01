# Caesar Cipher Encryption/Decryption App

A Python desktop application for encrypting and decrypting text using the Caesar cipher and ROT13 algorithms. Built with Flet framework.

## Features

- Caesar cipher encryption with customizable shift value
- ROT13 encryption
- Support for both alphabetic and extended character sets (including numbers)
- File upload and export capabilities
- Clean and intuitive GUI interface

## Requirements

- Python 3.6 or higher
- Flet library (`pip install flet`)

## Installation

1. Install Python from [python.org](https://python.org)
2. Install Flet:
   ```bash
   pip install flet
   ```
3. Download the application code (`caesar_cipher.py`)

## Usage

1. Run the application:
   ```bash
   python caesar.py
   ```

2. Basic Operations:
   - Enter text in the message field
   - (Optional) Enter a shift value (random if left blank)
   - Choose character set (Alphabet Only or Letters + Digits + Special Characters)
   - Click "Encrypt" to encrypt your message
   - Click "Decrypt" to decrypt the message
   - Click "Apply ROT13" for ROT13 encryption

3. Additional Features:
   - "Upload File": Load text from a .txt file
   - "Export": Save encrypted text to a file
   - "Clear": Reset all fields

## Tips

- For Caesar cipher, use the same shift value for encryption and decryption
- ROT13 is its own inverse - applying it twice returns the original text
- Extended character set also encrypts numbers
- Leave shift value empty for random shift encryption

## Notes

- The application automatically handles both Caesar cipher and ROT13 decryption
- Exported files are saved in .txt format
- Special characters remain unchanged in the basic alphabet mode
