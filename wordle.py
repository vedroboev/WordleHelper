import re
from rich.console import Console

console = Console()

words = []
with open("wordle.txt", "r") as file:
    for line in file:
        words.append(line.strip())


# Sorts selected words by the number of yellow letters.
def sort_by_yellow_letters(word: str, yellow_letters: set):
    count = 0
    for i in yellow_letters:
        if i in word:
            count += 1
    return count


# Format word into a rich-printable format according to letter colors.
def color_word(word: str, letters: dict) -> str:
    new_word = ""
    for letter in word:
        if color := letters.get(letter):
            new_word += f"[{color}]{letter}[/{color}]"
        else:
            new_word += letter
    return new_word


# TODO make a main method.
# TODO reformulate instruction statements.
while True:
    print("Analysing word...")
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

    # TODO can just use the keys even when green letters are added.
    yellow_letter_set = set()
    for letter in letters:
        yellow_letter_set.add(letter)

    # Getting green letters as a string.
    print("Enter the green letters and their positions. Example: ..a.c")

    green = input()
    if len(green) != 5:
        green == "....."

    for letter in green:
        if letter != ".":
            letters[letter] = "green"

    print("Enter excluded letters without spaces (optional). Example: rhgsfj:")
    excluded = input()

    # Forming regex. TODO move to separate function.
    regex = ""
    for i in range(5):
        if len(yellow[i]) != 0 or len(excluded) != 0:
            # Excludes words with yellow letter on this spot + excluded letters.
            regex += "(?![" + "".join(yellow[i]) + "".join(excluded) + "])"
        if green[i] == ".":
            # Allowing all letters if no information is given.
            regex += "[a-z]"
        else:
            # Allowing only green letters on the spot.
            regex += "[" + green[i] + "]"
    rex = re.compile(regex)

    print(regex)

    # Optimise all the sorting here.
    matches = list(filter(rex.match, words))
    matches.sort(key=lambda x: sort_by_yellow_letters(x, yellow_letter_set))

    print("Found {} matches:".format(len(matches)))
    prev_count = -1
    for word in matches:
        if sort_by_yellow_letters(word, yellow_letter_set) != prev_count:
            print(
                "\n-------------[{} YELLOW]-------------".format(
                    sort_by_yellow_letters(word, yellow_letter_set)
                )
            )
            prev_count = sort_by_yellow_letters(word, yellow_letter_set)

        console.print(color_word(word, letters))
