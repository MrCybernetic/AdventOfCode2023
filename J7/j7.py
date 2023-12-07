STRENGTH_ORDER_PART1 = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
STRENGTH_ORDER_PART2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
POKER_RULES = ["five_of_a_kind", "four_of_a_kind", "full_house", "three_of_a_kind", "two_pairs", "one_pair", "high_card"]


class CardsHand:
    def __init__(self, string_def: str) -> None:
        self.content = [card for card in string_def.split(' ')[0].split()[0]]
        self.bid = string_def.split(' ')[1]
        self.hand_type_strength = self._get_strength()

    def __repr__(self) -> str:
        return f"{self.content} {self.bid}"

    def _get_hand_type(self) -> str:
        """Returns the type of hand"""
        nb_of_occurence = []
        for first_card in self.content:
            number_found = 0
            for other_card in self.content:
                if first_card == other_card:
                    number_found += 1
            nb_of_occurence.append(number_found)
        if len(nb_of_occurence) > 1:
            if nb_of_occurence.count(2) == 2 and nb_of_occurence.count(3) == 3:
                return "full_house"
            elif nb_of_occurence.count(2) == 4:
                return "two_pairs"
            elif 3 in nb_of_occurence:
                return "three_of_a_kind"
            elif 2 in nb_of_occurence:
                return "one_pair"
            elif 4 in nb_of_occurence:
                return "four_of_a_kind"
            elif 5 in nb_of_occurence:
                return "five_of_a_kind"
            else:
                return "high_card"

    def get_hand_type_strength_for_part2(self) -> int:
        for index, card in enumerate(self.content):
            if card == "J":
                for letter in "AKQT98765432":
                    previous_card = self.content[index]
                    self.content[index] = letter
                    if (self._get_strength() >= self.hand_type_strength and self.content.count(letter) <= 4):
                        self.hand_type_strength = self._get_strength()
                    else:
                        self.content[index] = previous_card
        return self.hand_type_strength

    def _get_strength(self) -> int:
        """Returns the strength of the hand"""
        return (5-POKER_RULES.index(self._get_hand_type()))


def get_total_winning(deck: list[CardsHand], part_number: int) -> int:
    if part_number == 1:
        strength_order = STRENGTH_ORDER_PART1
    elif part_number == 2:
        strength_order = STRENGTH_ORDER_PART2
    for index in range(5):
        deck.sort(key=lambda x: strength_order.index(x.content[-index-1]), reverse=True)
    if part_number == 1:
        deck.sort(key=lambda x: x.hand_type_strength)
    elif part_number == 2:
        deck.sort(key=lambda x: x.get_hand_type_strength_for_part2())
    total_winning = 0
    for index, hands in enumerate(deck):
        total_winning += (index+1)*int(hands.bid)
    return total_winning


def main():
    # Part 1
    test_deck = []
    with open("J7/sample_test.txt", 'r') as file:
        for line in file:
            test_deck.append(CardsHand(line))
    assert (get_total_winning(test_deck, 1) == 6440)
    deck = []
    with open("J7/puzzle_input.txt", 'r') as file:
        for line in file:
            deck.append(CardsHand(line))
    print(get_total_winning(deck, 1))
    # Part 2
    assert (get_total_winning(test_deck, 2) == 5905)  # Passed
    print(get_total_winning(deck, 2))  # Failed


if __name__ == "__main__":
    main()
