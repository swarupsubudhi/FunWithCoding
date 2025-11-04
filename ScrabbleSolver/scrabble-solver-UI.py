# SCRABBLE Word Finder v0.1 #
import tkinter as tk
from tkinter import messagebox
from collections import Counter
import urllib.request

# --- Scrabble scoring ---
SCRABBLE_SCORES = {
    **{ch: 1 for ch in "AEILNORSTU"},
    **{ch: 2 for ch in "DG"},
    **{ch: 3 for ch in "BCMP"},
    **{ch: 4 for ch in "FHVWY"},
    **{ch: 5 for ch in "K"},
    **{ch: 8 for ch in "JX"},
    **{ch: 10 for ch in "QZ"},
}

def word_score(word):
    return sum(SCRABBLE_SCORES.get(ch.upper(), 0) for ch in word)

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
            valid_words.append((word, word_score(word)))

    return sorted(valid_words, key=lambda w: (-w[1], -len(w[0]), w[0]))

# --- GUI Logic ---
def run_solver():
    # Collect only non-empty letter entries
    letters = [entry.get().strip().lower() for entry in letter_entries if entry.get().strip() != ""]
    n = len(letters)

    if not (3 <= n <= 7):
        messagebox.showerror("Error", "Please enter between 3 and 7 letters.")
        return

    # Validate each letter
    for i, ch in enumerate(letters, start=1):
        if len(ch) != 1 or not ch.isalpha():
            messagebox.showerror("Error", f"Letter {i} is invalid. Enter a single alphabetic character.")
            return

    letters = "".join(letters)
    results = scrabble_solver(letters, dictionary)

    # Clear previous results
    for widget in results_frame.winfo_children():
        widget.destroy()

    if results:
        half = (len(results) + 1) // 2
        col1, col2 = results[:half], results[half:]

        col1_frame = tk.Frame(results_frame, bg="#ffffff")
        col1_frame.grid(row=0, column=0, sticky="n")
        for word, score in col1:
            tk.Label(col1_frame, text=f"{word} ({score})", font=("Courier New", 11),
                     anchor="w", bg="#ffffff", fg="#333333").pack(anchor="w")

        col2_frame = tk.Frame(results_frame, bg="#ffffff")
        col2_frame.grid(row=0, column=1, sticky="n", padx=15)
        for word, score in col2:
            tk.Label(col2_frame, text=f"{word} ({score})", font=("Courier New", 11),
                     anchor="w", bg="#ffffff", fg="#333333").pack(anchor="w")
    else:
        tk.Label(results_frame, text="No valid words found.", font=("Arial", 12),
                 bg="#ffffff", fg="red").pack()

# --- Validation for single letter ---
def validate_letter(P):
    return (len(P) <= 1 and (P == "" or P.isalpha()))

# --- Main Window ---
root = tk.Tk()
root.title("🎲 Scrabble Solver")
root.geometry("400x600")
root.configure(bg="#f0f4f7")

# --- Header ---
header = tk.Label(root, text="Scrabble Solver", font=("Helvetica", 18, "bold"),
                  bg="#4a90e2", fg="white", pady=8)
header.pack(fill="x")

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#f0f4f7")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter the letters:", bg="#f0f4f7", font=("Arial", 12)).pack(anchor="w", pady=(10,2))

letters_frame = tk.Frame(input_frame, bg="#f0f4f7")
letters_frame.pack()

vcmd_letter = (root.register(validate_letter), "%P")
letter_entries = []
for i in range(7):
    entry = tk.Entry(letters_frame, width=3, font=("Arial", 14), justify="center",
                     validate="key", validatecommand=vcmd_letter)
    entry.grid(row=0, column=i, padx=4)
    letter_entries.append(entry)

# --- Button ---
run_button = tk.Button(root, text="Find Words", command=run_solver,
                       bg="#4a90e2", fg="white", font=("Arial", 13, "bold"),
                       activebackground="#357ABD", activeforeground="white")
run_button.pack(pady=10)

# --- Results Frame ---
results_frame = tk.Frame(root, bg="#ffffff")
results_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Load dictionary once at startup
dictionary = load_dictionary(source="github")

root.mainloop()
