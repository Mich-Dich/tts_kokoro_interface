# utilities.py
import re

def extract_trailing_number(s):
    match = re.search(r"\d+$", s)
    return int(match.group()) if match else None

# ... other helper functions