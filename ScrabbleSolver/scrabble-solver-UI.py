# --- Scrabble Word Finder v0.1 --- #
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
        if 2 <= len(word) <= len(letters) and can_form(word, letters_count):
            valid_words.append((word, word_score(word)))

    return sorted(valid_words, key=lambda w: (-w[1], -len(w[0]), w[0]))

# --- GUI Logic ---
def run_solver():
    letters = [entry.get().strip().lower() for entry in letter_entries if entry.get().strip() != ""]
    n = len(letters)

    if not (2 <= n <= 12):
        messagebox.showerror("Error", "Please enter between 2 and 12 letters.")
        return

    for i, ch in enumerate(letters, start=1):
        if len(ch) != 1 or not ch.isalpha():
            messagebox.showerror("Error", f"Letter {i} is invalid. Enter a single alphabetic character.")
            return

    letters = "".join(letters)
    results = scrabble_solver(letters, dictionary)

    for widget in results_content.winfo_children():
        widget.destroy()

    if results:
        half = (len(results) + 1) // 2
        col1, col2 = results[:half], results[half:]

        col1_frame = tk.Frame(results_content, bg="#ffffff")
        col1_frame.grid(row=0, column=0, sticky="nw")
        for word, score in col1:
            tk.Label(col1_frame, text=f"{word} ({score})", font=("Courier New", 11),
                     anchor="w", bg="#ffffff", fg="#333333").pack(anchor="w")

        col2_frame = tk.Frame(results_content, bg="#ffffff")
        col2_frame.grid(row=0, column=1, sticky="nw", padx=15)
        for word, score in col2:
            tk.Label(col2_frame, text=f"{word} ({score})", font=("Courier New", 11),
                     anchor="w", bg="#ffffff", fg="#333333").pack(anchor="w")
    else:
        tk.Label(results_content, text="No valid words found.", font=("Arial", 12),
                 bg="#ffffff", fg="red").grid(row=0, column=0, sticky="w")

    results_content.update_idletasks()
    results_canvas.configure(scrollregion=results_canvas.bbox("all"))

# --- Validation for single letter ---
def validate_letter(P):
    return (len(P) <= 1 and (P == "" or P.isalpha()))

# --- Auto-advance focus ---
def auto_advance(event, idx):
    text = event.widget.get()
    if len(text) == 1 and text.isalpha():
        if idx + 1 < len(letter_entries):
            letter_entries[idx + 1].focus_set()

# --- Main Window ---
root = tk.Tk()
root.title("🎲 Scrabble Solver")
root.geometry("300x500")
root.configure(bg="#f0f4f7")

header = tk.Label(root, text="Scrabble Solver", font=("Helvetica", 18, "bold"),
                  bg="#4a90e2", fg="white", pady=8)
header.pack(fill="x")

input_frame = tk.Frame(root, bg="#f0f4f7")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter the letters (2–12):", bg="#f0f4f7", font=("Arial", 12)).pack(anchor="w", pady=(10,2))

letters_frame = tk.Frame(input_frame, bg="#f0f4f7")
letters_frame.pack()

vcmd_letter = (root.register(validate_letter), "%P")
letter_entries = []
# Arrange 12 entries in a 6x2 grid
for i in range(12):
    row, col = divmod(i, 6)
    entry = tk.Entry(letters_frame, width=3, font=("Arial", 14), justify="center",
                     validate="key", validatecommand=vcmd_letter)
    entry.grid(row=row, column=col, padx=4, pady=4)
    entry.bind("<KeyRelease>", lambda e, idx=i: auto_advance(e, idx))
    letter_entries.append(entry)

run_button = tk.Button(root, text="Find Words", command=run_solver,
                       bg="#4a90e2", fg="white", font=("Arial", 13, "bold"),
                       activebackground="#357ABD", activeforeground="white")
run_button.pack(pady=10)

# --- Scrollable Results ---
results_outer = tk.Frame(root, bg="#ffffff")
results_outer.pack(padx=10, pady=10, fill="both", expand=True)

results_canvas = tk.Canvas(results_outer, bg="#ffffff", highlightthickness=1, highlightbackground="#dddddd")
results_canvas.grid(row=0, column=0, sticky="nw")

scrollbar = tk.Scrollbar(results_outer, orient="vertical", command=results_canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
results_canvas.configure(yscrollcommand=scrollbar.set)

results_content = tk.Frame(results_canvas, bg="#ffffff")
results_window = results_canvas.create_window((0, 0), window=results_content, anchor="nw")

def _on_mousewheel(event):
    if event.num == 5 or event.delta < 0:
        results_canvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta > 0:
        results_canvas.yview_scroll(-1, "units")

results_canvas.bind_all("<MouseWheel>", _on_mousewheel)
results_canvas.bind_all("<Button-4>", _on_mousewheel)
results_canvas.bind_all("<Button-5>", _on_mousewheel)

def _configure_results_content(event):
    results_canvas.configure(scrollregion=results_canvas.bbox("all"))
results_content.bind("<Configure>", _configure_results_content)

dictionary = load_dictionary(source="github")

root.mainloop()
