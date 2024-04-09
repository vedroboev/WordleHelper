import re
from rich.console import Console

# TODO make it possible to work with both russian and english.
# TODO switch all prints to console.print
console = Console()

# TODO do inside the main method.
words = []
with open("wordle_ru.txt", "r") as file:
    for line in file:
        words.append(line.strip())


# TODO update python, add proper type annotation.
# Formats word to be rich-printable, returns word + number of yellow letters.
def color_word(word: str, letters: dict):
    new_word = ""
    yellow_letters = 0

    for letter in word:
        if color := letters.get(letter):
            new_word += f"[{color}]{letter}[/{color}]"
            if color == "yellow":
                yellow_letters += 1
        else:
            new_word += letter

    return new_word, yellow_letters


# TODO update Python, add proper type annotations.
def build_regex(green, yellow, excluded, lookahead = None) -> str:
    regex = lookahead if lookahead else ""

    excluded = "".join(excluded)

    for i in range(len(green)):
        if green[i] != ".":
            regex += f"[{green[i]}]"
        elif len(yellow[i]) != 0:
            # TODO what happens if yellow & excluded letters intersect?
            regex += f"[^{''.join(yellow[i])}{excluded}]"
        elif len(excluded) != 0:
            regex += f"[^{excluded}]"
        else:
            regex += "[.]"

    return regex


# TODO make a main method.
# TODO add a feature to find the most optimal first words.
# TODO reformulate instruction statements
# TODO add command to exit program.
while True:
    print("\n\nAnalysing word...")
    print('To skip to next input step, you can input "."')

    # Dict used to store all letters with color.
    letters = {}

    # Collecting yellow letters from all different guesses.
    yellow = [set() for _ in range(5)]
    print("Enter all the yellow letters and their positions. Example: yy.y.")
    while (word := input()) != ".":
        for i, letter in enumerate(word):
            if letter != ".":
                yellow[i].add(letter)
                letters[letter] = "yellow"

    # Getting green letters as a string.
    print("Enter the green letters and their positions. Example: ..a.c")

    green = input()
    if len(green) != 5:
        green = "....."

    for letter in green:
        if letter != ".":
            letters[letter] = "green"

    print("Enter excluded letters without spaces (optional). Example: rhgsfj:")
    excluded = input()

    # Forming regex. TODO move to separate function.
    regex = build_regex(green, yellow, excluded)
    rex = re.compile(regex)

    matches = list(filter(rex.match, words))
    matches_by_letters = {i: set() for i in range(0, 6)}

    print("Found {} matches:".format(len(matches)))

    for match in matches:
        match_colored, matched_letters = color_word(match, letters)
        matches_by_letters[matched_letters].add(match_colored)

    # TODO print / find less matches, only include ones with at least all yellow letters.
    for letter_count, matched_words in matches_by_letters.items():
        if matched_words:
            console.print(f"[{letter_count} YELLOW]", style="red on yellow")
            for word in matched_words:
                console.print(word)
