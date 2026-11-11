
import json
from pathlib import Path
import copy



#validation function
def validate(data):
    return false










# Reads the input DFA
try:
    with open("input_dfa.json", "r") as file:
        data = json.load(file)

# if the DFA is invalid or does not exist, print an exception
except json.JSONDecodeError:
    print("[ERROR] Invalid JSON formatting.")

except FileNotFoundError:
    print("[ERROR] Input file not found.")



# LOGIC

# Checks for valid DFA
is_valid = False


#if not valid, print an error
if not is_valid:
    print("[ERROR] Invalid DFA.")

#if the DFA is valid, perform the logic and print the complement
else:
    # Prints a formatted message showing the original vs. changed DFA
    print("Original DFA:")
    print(json.dumps(data, indent=4))

    print()

    print("Complement DFA:")
