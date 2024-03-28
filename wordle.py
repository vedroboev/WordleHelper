import re
from rich.console import Console

yellow_letters = set()
console = Console()

words = []
with open('wordle.txt', 'r') as file:
    for line in file:
        words.append(line.strip())

# Sorts selected words by the number of yellow letters.
def sorter(x):
    global yellow_letters
    count = 0
    for i in yellow_letters:
        if i in x:
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


while True:
    print("Analysing word...")

    green = []
    print("Enter the green letters and their positions. Example: ..a.c")

    word = input()
    for letter in word:
        green.append("" if letter == "." else letter)

    yellow = [[] for _ in range(5)]
    yellow_letters = set()
    print("Enter the yellow letters and their positions Enter . when done. Example: yy.y.")

    word = ""
    while (word := input()) != ".":
        for i, letter in enumerate(word):
            if letter != ".":
                yellow[i].append(letter)
                yellow_letters.add(letter)

    print("Enter excluded letters separated by space (optional):")
    excluded = input()

    # Forming regex.
    regex = ""
    for i in range(5):
        if len(yellow[i]) != 0 or len(excluded) != 0:
            # Excludes words with yellow letter on this spot + excluded letters.
            regex += "(?![" + "".join(yellow[i]) + "".join(excluded) + "])"
        if green[i] == "":
            # Allowing all letters if no information is given.
            regex += "[a-z]"
        else:
            # Allowing only green letters on the spot.
            regex += "[" + green[i] + "]"

    # TODO Temporar! Remake
    letters = {letter: "green" for letter in green}
    letters |= {letter: "yellow" for letter in yellow_letters}

    print(regex)
    rex = re.compile(regex)
    matches = list(filter(rex.match, words))
    matches.sort(key=sorter)

    print("Found {} matches:".format(len(matches)))
    prev_count = -1
    for word in matches:
        if sorter(word) != prev_count:
            print(
                "\n-------------[{} YELLOW]-------------".format(sorter(word)))
            prev_count = sorter(word)

        console.print(color_word(word, letters))

