DIGIT_SPELLED = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def find_all_digits(text: str) -> list[int, int]:
    digits_array = []
    # Search spelled digits
    if search_spelled_digits(text) is not None:
        digits_array.extend(search_spelled_digits(text))
    # Search digits
    if search_numeral_digits(text) is not None:
        digits_array.extend(search_numeral_digits(text))
    # Sort digits by position
    digits_array.sort(key=lambda x: x[1])
    return digits_array


def search_spelled_digits(text: str) -> list[int, int]:
    spelled_digits_array = []
    word_to_seach = DIGIT_SPELLED.copy()
    while len(word_to_seach) > 0:
        word = word_to_seach.pop(0)
        start_index = 0
        while True:
            index = text.find(word, start_index)
            if index == -1:
                break
            else:
                spelled_digits_array.append([DIGIT_SPELLED.index(word) + 1, index])
                start_index = index + len(word)
    if len(spelled_digits_array) == 0:
        return None
    else:
        return spelled_digits_array


def search_numeral_digits(text: str) -> list[int, int]:
    numeral_digits_array = []
    for index, caracter in enumerate(text):
        if caracter.isdigit():
            numeral_digits_array.append([int(caracter), index])
    if len(numeral_digits_array) == 0:
        return None
    else:
        return numeral_digits_array


def get_text_from_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def find_calib_value(line: str) -> int:
    digits_array = find_all_digits(line)
    if len(digits_array) == 0:
        return 0
    else:
        first_digit = digits_array[0][0]
        last_digit = digits_array[-1][0]
        calib_value = int(str(first_digit) + str(last_digit))
        return calib_value


def main(text_path: str) -> int:
    calibration_values = []
    text = get_text_from_file(text_path)
    for line in text.splitlines():
        calibration_values.append(find_calib_value(line))
    return sum(calibration_values)


if __name__ == '__main__':
    test = False
    if test:
        # print(main("J1/test_sample_part2.txt"))
        # print(main("J1/test_sample.txt"))
        print(main("J1/test_spelled.txt"))
    else:
        print(main('J1/puzzle_input.txt'))
