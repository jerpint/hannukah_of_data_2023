import pandas as pd


keypad_map = {
    "abc": 2,
    "def": 3,
    "ghi": 4,
    "jkl": 5,
    "mno": 6,
    "pqrs": 7,
    "tuv": 8,
    "wxyz": 9,
}

# expand to dict by letter for easier use
letter_to_digit = {
    letter: digit for letters, digit in keypad_map.items() for letter in letters
}


def name_to_digits(name: str) -> list[int]:
    digits = []
    for letter in name:
        letter = letter.lower()
        digits.append(letter_to_digit.get(letter, "-1"))
    return digits


def digits_to_number(digits: list[int]) -> str:
    if len(digits) != 10:
        # invalid phone number, don't bother processing
        return None
    digits_1 = "".join([str(d) for d in digits[0:3]])
    digits_2 = "".join([str(d) for d in digits[3:6]])
    digits_3 = "".join([str(d) for d in digits[6:]])
    return f"{digits_1}-{digits_2}-{digits_3}"


def name_to_phone(name: str) -> str:
    return digits_to_number(name_to_digits(name))


df = pd.read_csv("./data/5784/noahs-customers.csv")
df["phone_from_name"] = df.name.apply(lambda name: name_to_phone(name.split()[-1]))

print(df[df.phone == df.phone_from_name])
