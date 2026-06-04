import random
import string

def generate_text_file(filename, length):
    chars = string.ascii_letters + ' '  # All alphabets + space
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(length):
            f.write(random.choice(chars))

# Example: generate a file with 1 million characters
generate_text_file('long_text.txt', 10**3)
print("Generated")
