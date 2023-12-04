import re


class Card:
    def __init__(self, number: int, winning_numbers: list[int], numbers_got: list[int]):
        self.number = number
        self.winning_numbers = winning_numbers
        self.numbers_got = numbers_got

    def __repr__(self):
        return f"Card(number: {self.number}, winning_numbers: {self.winning_numbers}, numbers_got: {self.numbers_got})"

    def get_score(self) -> int:
        """Return the score of the card."""
        number_of_winning_numbers = len(self.get_winning_numbers_got())
        if number_of_winning_numbers == 0:
            return 0
        else:
            return pow(2, number_of_winning_numbers-1)

    def get_winning_numbers_got(self) -> list[int]:
        """Return the winning numbers of the card you got."""
        winning_numbers_got = []
        for number in self.numbers_got:
            if number in self.winning_numbers:
                winning_numbers_got.append(number)
        return winning_numbers_got

    def get_number_of_winning_numbers_got(self) -> int:
        """Return the number of winning numbers of the card you got."""
        return len(self.get_winning_numbers_got())


def get_cards_from_file(file_path: str) -> list[Card]:
    """Return the cards from the file."""
    cards = []
    with open(file_path, "r") as file:
        for line in file:
            number = int(re.search(r"Card\s+(\d+):", line).group(1))
            winning_numbers = list(map(int, re.findall(r"\d+", line.split(":")[1].split("|")[0])))
            numbers_got = list(map(int, re.findall(r"\d+", line.split("|")[1])))
            cards.append(Card(number, winning_numbers, numbers_got))
    return cards


def main():
    # Part 1
    cards = get_cards_from_file("J4/puzzle_input.txt")
    scores = []
    for card in cards:
        scores.append(card.get_score())
    print(sum(scores))
    # Part 2
    for card in cards:
        for number in range(0, card.get_number_of_winning_numbers_got()):
            cards.append(Card(cards[card.number+number].number, cards[card.number+number].winning_numbers, cards[card.number+number].numbers_got))
    print(len(cards))


if __name__ == "__main__":
    main()
