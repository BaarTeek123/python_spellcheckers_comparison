import random
import re
import string

from Sentence_Generator.Key import get_close_key_error


def transpose(word: str) -> str:
    """Function that transposes chars in the word."""
    if len(word) >= 3:
        x = random.randint(0, len(word) - 2)
        if word[x] == word[x + 1]:
            while word[x] != word[x + 1]:
                x = random.randint(0, len(word) - 2)
        word = list(word)
        word[x], word[x + 1] = word[x + 1], word[x]
        return "".join(word)


def deletion(word: str) -> str:
    """Function that deletes a char in the word."""
    if len(word) >= 3:
        x = random.randint(0, len(word) - 1)
        if x > 0:
            return word[:x - 1] + word[x:]
        else:
            return word[1:]


def replace(word: str, randomly: bool = False, key_map_option: int = 0) -> str:
    """Function that replaces a char in the word."""
    i = 0
    while True:
        idx = random.randint(0, len(word) - 1)
        word = list(word)
        print(f"Replave while True = {word[idx]}")

        if randomly:
            word[idx] = random.choice(re.sub(r'[\s]', '', string.printable))
            return "".join(word)
        elif not randomly and word[idx].isalpha():
            word[idx] = get_close_key_error(word[idx].upper(), key_map_option)
            return "".join(word)
        i += 1
        if i ==5:
            randomly = True


def insert(word: str, randomly: bool = False, key_map_option: int = 0) -> str:
    print("insert while True")

    """Function that inserts a char in the word."""
    i = 0
    while True:
        idx = random.randint(0, len(word))
        if randomly:
            return word[:idx] + random.choice(re.sub(r'[\s]', '', string.printable)) + word[idx:]
        else:
            word = list(word)
            if idx == len(word) and word[idx-1].isalpha():
                word.insert(idx, get_close_key_error(word[idx-1].upper(), key_map_option))
                return "".join(word)
            elif idx < len(word) and word[idx].isalpha():
                word.insert(idx, get_close_key_error(word[idx].upper(), key_map_option))
                return "".join(word)
        i += 1
        if i == 5:
            randomly = True
            word = "".join(word)



def misspell_sentence(sentence: str, amount_of_misspells: int = 1, randomly: bool = False):
    """Function that misspells the sentence."""
    operations = {'transpose': 0, 'replace': 0, 'deletion': 0, 'insert': 0}
    if len(sentence) > amount_of_misspells and amount_of_misspells>0:
        while amount_of_misspells > 0:
            operation_choice = random.randint(1, 4)
            if isinstance(sentence, str):
                sentence = sentence.split()
            word_choice = random.randint(0, len(sentence) - 1)
            if operation_choice == 0 and len(sentence[word_choice]) > 2:
                sentence[word_choice] = transpose(sentence[word_choice])
                amount_of_misspells -= 1
                operations['transpose'] += 1
            elif operation_choice == 1 and len(sentence[word_choice]) >= 2:
                sentence[word_choice] = replace(sentence[word_choice], randomly)
                amount_of_misspells -= 1
                operations['replace'] += 1

            elif operation_choice == 2 and len(sentence[word_choice]) > 2:
                sentence[word_choice] = deletion(sentence[word_choice])
                amount_of_misspells -= 1
                operations['deletion'] += 1

            elif operation_choice == 3:
                sentence[word_choice] = insert(sentence[word_choice], randomly)
                amount_of_misspells -= 1
                operations['insert'] += 1

        return ' '.join(sentence), operations

    return sentence, operations

