import re
from rich.console import Console
from rich.prompt import Prompt, Confirm


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

    # TODO simplify prompts if user already ran a program.
    console.rule("ANALYSING WORD")
    console.print(
        "You can press [red]Enter[/] or [red].[/] at each step to skip it.", end="\n\n"
    )

    # Dict used to store all letters with color.
    letters = {}

    console.print("Enter all the [yellow]yellow letters[/] at their positions")
    console.print("Enter yellow letters in each guess [u]separately[/].")
    console.print("Example: .[yellow]c[/].[yellow]a[/][yellow]r[/]")

    # Collecting yellow letters from all different guesses.
    yellow = [set() for _ in range(5)]
    while (word := input()) and word != ".":
        for i, letter in enumerate(word):
            if letter != ".":
                yellow[i].add(letter)
                letters[letter] = "yellow"

    console.print("Enter [u]all[/] the [green]green letters[/] at their positions")
    console.print("Example: [green]c[/].[green]a[/]..")

    # Getting green letters as a string.
    green = input()
    if len(green) != 5:
        green = "....."
    else:
        console.print("")

    for letter in green:
        if letter != ".":
            letters[letter] = "green"

    console.print("Enter [u]all[/] excluded letters without spaces (optional).")
    console.print("Example: [white]othils[white]")

    excluded = input().strip(". ")

    lookahead = build_yellow_letter_lookahead(letters)
    regex = build_regex(yellow, green, excluded, lookahead=lookahead)
    rex = re.compile(regex)

    matches = list(filter(rex.match, words))
    matches_by_letters = {i: set() for i in range(0, 6)}

    console.rule(f"FOUND {len(matches)} MATCHES:")

    for match in matches:
        match_colored, matched_letters = color_word(match, letters)
        matches_by_letters[matched_letters].add(match_colored)

    # TODO print in multiple columns instead of one big one.
    for letter_count, matched_words in matches_by_letters.items():
        if matched_words:
            console.print(f"[red on yellow][{letter_count} YELLOW][/]")
            for word in matched_words:
                console.print(word)


# TODO add a feature to find the most optimal first words.
def main():
    """Runs script in a loop."""

    console = Console()

    LANGUAGES = dict(ru="wordle_ru.txt", en="wordle.txt")
    LANGUAGE_NAMES = dict(ru="Russian", en="English")

    language = Prompt.ask("Select a language", choices=["ru", "en"], default="en")

    console.clear()
    console.print(f"[yellow bold]{LANGUAGE_NAMES[language]}[/] language selected.")

    words = []
    with open(LANGUAGES[language], "r") as file:
        for line in file:
            words.append(line.strip())

    while True:
        # TODO switch languages between iterations.
        run_helper(console=console, words=words)

        if not Confirm.ask("Do you want to continue?"):
            return

        console.clear()


if __name__ == "__main__":
    main()
