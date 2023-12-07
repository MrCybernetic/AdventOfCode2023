STRENGTH_ORDER = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
POKER_RULES = ["five_of_a_kind", "four_of_a_kind", "full_house", "three_of_a_kind", "two_pairs", "one_pair", "high_card"]


class CardsHand:
    def __init__(self, string_def: str) -> None:
        self.content = [card for card in string_def.split(' ')[0].split()[0]]
        self.bid = string_def.split(' ')[1]
        self.hand_type = self._get_hand_type()
        self.hand_type_strength = 5-POKER_RULES.index(self.hand_type)

    def __repr__(self) -> str:
        return f"{self.content} {self.bid}"

    def _get_hand_type(self) -> str:
        """Returns the type of hand"""
        nv_of_occurence = []
        for first_card in self.content:
            number_found = 0
            for other_card in self.content:
                if first_card == other_card:
                    number_found += 1
            nv_of_occurence.append(number_found)
        if len(nv_of_occurence) > 1:
            if nv_of_occurence.count(2) == 2 and nv_of_occurence.count(3) == 3:
                return "full_house"
            elif nv_of_occurence.count(2) == 4:
                return "two_pairs"
            elif 3 in nv_of_occurence:
                return "three_of_a_kind"
            elif 2 in nv_of_occurence:
                return "one_pair"
            elif 4 in nv_of_occurence:
                return "four_of_a_kind"
            elif 5 in nv_of_occurence:
                return "five_of_a_kind"
            else:
                return "high_card"


def get_total_winning(deck: list[CardsHand]) -> int:
    for index in range(5):
        deck.sort(key=lambda x: STRENGTH_ORDER.index(x.content[-index-1]), reverse=True)
    deck.sort(key=lambda x: x.hand_type_strength)
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
    assert (get_total_winning(test_deck) == 6440)
    deck = []
    with open("J7/puzzle_input.txt", 'r') as file:
        for line in file:
            deck.append(CardsHand(line))
    print(get_total_winning(deck))
    # Part 2


if __name__ == "__main__":
    main()
