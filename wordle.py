import re
from rich.console import Console


def color_word(word: str, letters: dict) -> tuple[str, int]:
    """Format word to be rich-printable and count yellow letters"""
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


def build_regex(
    yellow: list[set[str]], green: str, excluded: str, lookahead: str = None
) -> str:
    """Build a regex to search for a word based on known letters"""
    regex = lookahead if lookahead else ""

    # TODO check for intersections & duplicate letters.
    for i in range(len(green)):
        if green[i] != ".":
            regex += f"[{green[i]}]"
        elif len(yellow[i]) != 0:
            regex += f"[^{''.join(yellow[i])}{excluded}]"
        elif len(excluded) != 0:
            regex += f"[^{excluded}]"
        else:
            regex += "."
    return regex


def build_yellow_letter_lookahead(letters: dict[str, str]) -> str:
    """Build a regex to ensure that all given letters are present in the word"""
    lookahead = ""
    for letter in letters:
        if letters[letter] == "yellow":
            lookahead += rf"(?=\w*[{letter}])"
    return lookahead


def run_helper(console: Console, words: list[str]):
    """Main loop, takes user input and finds appropriate words"""

    # TODO reformulate instruction statements
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
    excluded = input().strip(". ")

    lookahead = build_yellow_letter_lookahead(letters)
    regex = build_regex(yellow, green, excluded, lookahead=lookahead)
    rex = re.compile(regex)

    matches = list(filter(rex.match, words))
    matches_by_letters = {i: set() for i in range(0, 6)}

    print("Found {} matches:".format(len(matches)))

    for match in matches:
        match_colored, matched_letters = color_word(match, letters)
        matches_by_letters[matched_letters].add(match_colored)

    for letter_count, matched_words in matches_by_letters.items():
        if matched_words:
            console.print(f"[{letter_count} YELLOW]", style="red on yellow")
            for word in matched_words:
                console.print(word)


# TODO add a feature to find the most optimal first words.
# TODO add command to exit program.
def main():
    """Runs script in a loop."""

    # TODO make it possible to work with both russian and english.
    # TODO switch all prints to console.print
    console = Console()

    # TODO add ability to switch between languages.
    words = []
    with open("wordle.txt", "r") as file:
        for line in file:
            words.append(line.strip())

    while True:
        run_helper(console=console, words=words)


if __name__ == "__main__":
    main()
