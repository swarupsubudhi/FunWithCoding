from collections import Counter
import urllib.request

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

def main():
    try:
        n = int(input("Enter the number of letters (between 3 and 7): ").strip())
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if not (3 <= n <= 7):
        print("Number of letters must be between 3 and 7.")
        return

    letters = ""
    for i in range(n):
        while True:
            ch = input(f"Enter letter {i+1}: ").strip().lower()
            if len(ch) == 1 and ch.isalpha():
                letters += ch
                break
            else:
                print("Please enter a single alphabetic character.")

    dictionary = load_dictionary(source="github")
    results = scrabble_solver(letters, dictionary)

    if results:
        print("\nPossible words:")
        for word in results:
            print(word)
    else:
        print("No valid words found.")

if __name__ == "__main__":
    main()
