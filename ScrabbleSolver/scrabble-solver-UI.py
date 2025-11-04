import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import Counter
import urllib.request

# --- Dictionary Loader ---
def load_dictionary(source="github", file_path="words_alpha.txt"):
    if source == "local":
        with open(file_path, "r") as f:
            return set(word.strip().lower() for word in f)
    elif source == "github":
        url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")
        return set(word.strip().lower() for word in data.splitlines())
    else:
        raise ValueError("Invalid source. Use 'local' or 'github'.")

# --- Word Check ---
def can_form(word, letters_count):
    word_count = Counter(word)
    for ch, cnt in word_count.items():
        if letters_count[ch] < cnt:
            return False
    return True

def scrabble_solver(letters, dictionary):
    letters = letters.lower()
    letters_count = Counter(letters)
    valid_words = []

    for word in dictionary:
        if 3 <= len(word) <= len(letters) and can_form(word, letters_count):
            valid_words.append(word)

    return sorted(valid_words, key=lambda w: (-len(w), w))

# --- GUI Logic ---
def run_solver():
    try:
        n = int(num_letters_entry.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number between 3 and 7.")
        return

    if not (3 <= n <= 7):
        messagebox.showerror("Error", "Number of letters must be between 3 and 7.")
        return

    letters = []
    for i in range(n):
        ch = letter_entries[i].get().strip().lower()
        if len(ch) != 1 or not ch.isalpha():
            messagebox.showerror("Error", f"Letter {i+1} is invalid. Enter a single alphabetic character.")
            return
        letters.append(ch)

    letters = "".join(letters)
    results = scrabble_solver(letters, dictionary)

    output_box.delete(1.0, tk.END)
    if results:
        output_box.insert(tk.END, "\n".join(results))
    else:
        output_box.insert(tk.END, "No valid words found.")

# --- Main Window ---
root = tk.Tk()
root.title("Scrabble Solver")

# Number of letters
tk.Label(root, text="Number of letters (3–7):").grid(row=0, column=0, sticky="w")
num_letters_entry = tk.Entry(root, width=5)
num_letters_entry.grid(row=0, column=1, sticky="w")

# Letter entries
letter_entries = []
for i in range(7):
    tk.Label(root, text=f"Letter {i+1}:").grid(row=i+1, column=0, sticky="w")
    entry = tk.Entry(root, width=5)
    entry.grid(row=i+1, column=1, sticky="w")
    letter_entries.append(entry)

# Run button
run_button = tk.Button(root, text="Find Words", command=run_solver)
run_button.grid(row=8, column=0, columnspan=2, pady=10)

# Output box
output_box = scrolledtext.ScrolledText(root, width=40, height=15)
output_box.grid(row=9, column=0, columnspan=2, pady=10)

# Load dictionary once at startup
dictionary = load_dictionary(source="github")

root.mainloop()
