from enum import Enum
import random

class Key:
    def __init__(self, sign, code, left_upper_key, right_upper_key, left_key, right_key, left_bottom_key,
                 right_bottom_key):
        self._sign = sign
        self._key_code = code
        self.left_upper_key = left_upper_key
        self.right_upper_key = right_upper_key
        self.left_key = left_key
        self.right_key = right_key
        self.left_bottom_key = left_bottom_key
        self.right_bottom_key = right_bottom_key

class Keys(Enum):
    A = Key(sign='a', code=None, left_upper_key='q', right_upper_key='w', left_key=None, right_key='s',
            left_bottom_key=None, right_bottom_key='z')

    B = Key(sign='b', code=None, left_upper_key='g', right_upper_key='h', left_key='v', right_key='n',
            left_bottom_key=' ', right_bottom_key=None)

    C = Key(sign='c', code=None, left_upper_key='d', right_upper_key='f', left_key='x', right_key='v',
            left_bottom_key=' ', right_bottom_key=None)

    D = Key(sign='d', code=None, left_upper_key='e', right_upper_key='r', left_key='s', right_key='f',
            left_bottom_key='x', right_bottom_key='c')

    E = Key(sign='e', code=None, left_upper_key='3', right_upper_key='4', left_key='w', right_key='r',
            left_bottom_key='s', right_bottom_key='d')

    F = Key(sign='f', code=None, left_upper_key='r', right_upper_key='t', left_key='d', right_key='g',
            left_bottom_key='c', right_bottom_key='v')

    G = Key(sign='g', code=None, left_upper_key='t', right_upper_key='y', left_key='f', right_key='h',
            left_bottom_key='v', right_bottom_key='b')

    H = Key(sign='h', code=None, left_upper_key='y', right_upper_key='u', left_key='g', right_key='j',
            left_bottom_key='b', right_bottom_key='n')

    I = Key(sign='i', code=None, left_upper_key='8', right_upper_key='9', left_key='u', right_key='o',
            left_bottom_key='j', right_bottom_key='k')

    J = Key(sign='j', code=None, left_upper_key='u', right_upper_key='i', left_key='h', right_key='k',
            left_bottom_key='n', right_bottom_key='m')

    K = Key(sign='k', code=None, left_upper_key='i', right_upper_key='o', left_key='j', right_key='l',
            left_bottom_key='m', right_bottom_key=',')

    L = Key(sign='l', code=None, left_upper_key='o', right_upper_key='p', left_key='k', right_key=';',
            left_bottom_key=',', right_bottom_key='.')

    M = Key(sign='m', code=None, left_upper_key='j', right_upper_key='k', left_key='n', right_key=',',
            left_bottom_key=' ', right_bottom_key=' ')

    N = Key(sign='n', code=None, left_upper_key='h', right_upper_key='j', left_key='b', right_key='m',
            left_bottom_key=' ', right_bottom_key=' ')

    O = Key(sign='o', code=None, left_upper_key='9', right_upper_key='0', left_key='i', right_key='p',
            left_bottom_key='k', right_bottom_key='l')

    P = Key(sign='p', code=None, left_upper_key='0', right_upper_key='-', left_key='o', right_key='[',
            left_bottom_key='l', right_bottom_key=';')

    Q = Key(sign='q', code=None, left_upper_key='1', right_upper_key='2', left_key=None, right_key='w',
            left_bottom_key='a', right_bottom_key='s')

    R = Key(sign='r', code=None, left_upper_key='4', right_upper_key='5', left_key='e', right_key='t',
            left_bottom_key='d', right_bottom_key='f')

    S = Key(sign='s', code=None, left_upper_key='w', right_upper_key='e', left_key='a', right_key='d',
            left_bottom_key='z', right_bottom_key='x')

    T = Key(sign='t', code=None, left_upper_key='5', right_upper_key='6', left_key='r', right_key='y',
            left_bottom_key='f', right_bottom_key='g')

    U = Key(sign='u', code=None, left_upper_key='7', right_upper_key='8', left_key='y', right_key='i',
            left_bottom_key='h', right_bottom_key='j')

    W = Key(sign='w', code=None, left_upper_key='2', right_upper_key='3', left_key='q', right_key='e',
            left_bottom_key='a', right_bottom_key='s')

    V = Key(sign='v', code=None, left_upper_key='f', right_upper_key='g', left_key='c', right_key='b',
            left_bottom_key=' ', right_bottom_key=' ')

    X = Key(sign='x', code=None, left_upper_key='s', right_upper_key='d', left_key='z', right_key='c',
            left_bottom_key=None, right_bottom_key=' ')

    Y = Key(sign='y', code=None, left_upper_key='6', right_upper_key='7', left_key='t', right_key='u',
            left_bottom_key='g', right_bottom_key='h')

    Z = Key(sign='z', code=None, left_upper_key='a', right_upper_key='s', left_key=None, right_key='x',
            left_bottom_key=None, right_bottom_key=None)


def get_close_key_error(letter: str, option: int = 0):
    """
    Option == 0 random choice from all options (for 'd' it's ['e', 'r', 's', 'f', 'x', 'c'])
    Option == 1 random choice from upper options (for 'd' it's ['e', 'r'])
    Option == 2 random choice from same level options (for 'd' it's ['s', 'f'])
    Option == 3 random choice from bottom options   for 'd' it's ['x', 'c'])
    """
    if option == 0:
        return str(random.choice([value for attribute, value in Keys[letter].value.__dict__.items() if attribute[:1] != '_' and value is not None]))
    elif option == 1:
        return str(random.choice([value for attribute, value in Keys[letter].value.__dict__.items() if
                                  attribute[:1] != '_' and 'upper' in attribute and value is not None]))
    elif option == 3:
        return str(random.choice([value for attribute, value in Keys[letter].value.__dict__.items() if
                              attribute[:1] != '_' and 'bottom' in attribute and value is not None]))
    else:
        return str(random.choice([value for attribute, value in Keys[letter].value.__dict__.items() if
                              attribute[:1] != '_' and attribute in ['left_key', 'right_key'] and value is not None]))


def get_close_key_map(original_char: str, misspelled_char: str):
    try:
        return [k for k, v in Keys[original_char.upper()].value.__dict__.items() if v == misspelled_char][0]
    except AttributeError:
        return original_char
    except IndexError:
        return None
    except Exception:
        return None










