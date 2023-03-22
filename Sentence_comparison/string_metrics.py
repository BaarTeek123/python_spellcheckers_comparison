import textdistance
from Sentence_Generator.Key import get_close_key_map


class EditOperation:

    def __init__(self, operation_type_name: str, operation_subtype_id: int, idx: int,
                 previous_char: str, next_char: str):
        self.operation_type_name = operation_type_name
        self.operation_subtype_id = operation_subtype_id  # (word start, middle of the word, end of word)
        self.previous_char = previous_char
        self.next_char = next_char
        self.char_idx = idx


class Insert(EditOperation):
    def __init__(self, operation_subtype_id: int, new_char: str, idx: int, previous_char: str, next_char: str):
        self.inserted_char = new_char
        self.close_key_previous = get_close_key_map(previous_char, self.inserted_char)
        self.close_key_next = get_close_key_map(previous_char, self.inserted_char)
        super().__init__(operation_type_name='Insert', operation_subtype_id=operation_subtype_id,
                         idx=idx, previous_char=previous_char, next_char=next_char)


class Delete(EditOperation):
    def __init__(self, operation_subtype_id: int, deleted_char: str, idx: int, previous_char: str, next_char: str):
        self.deleted_char = deleted_char
        super().__init__(operation_type_name='Delete', operation_subtype_id=operation_subtype_id,
                         idx=idx, previous_char=previous_char, next_char=next_char)

    def __repr__(self):
        return super().__repr__() + "\tdeleted char: " + self.deleted_char


class Replace(EditOperation):
    def __init__(self, operation_subtype_id: int, old_char: str, new_char: str, idx: int, previous_char: str,
                 next_char: str):
        self.old_char = old_char
        self.new_char = new_char
        print('  new char: ', self.new_char)
        print('old char: ', self.old_char)
        self.close_key = get_close_key_map(self.old_char, self.new_char)
        super().__init__(operation_type_name='Replace', operation_subtype_id=operation_subtype_id,
                         idx=idx, previous_char=previous_char, next_char=next_char)


class Transpose(EditOperation):
    def __init__(self, operation_subtype_id: int, left_char: str, right_char: str, idx_left: int, idx_right: int,
                 previous_char: str, next_char: str):
        self.left_char = left_char
        self.right_char = right_char
        self.idx_right = idx_right
        super().__init__(operation_type_name='Transpose', operation_subtype_id=operation_subtype_id,
                         idx=idx_left, previous_char=previous_char, next_char=next_char)


def get_damerau_levenshtein_distance_matrix(word_1: str, word_2: str, is_damerau: bool = False):
    distance_matrix = [[0 for _ in range(len(word_2) + 1)] for _ in range(len(word_1) + 1)]
    for i in range(len(word_1) + 1):
        distance_matrix[i][0] = i
    for j in range(len(word_2) + 1):
        distance_matrix[0][j] = j
    for i in range(len(word_1)):
        for j in range(len(word_2)):
            if word_1[i] == word_2[j]:
                cost = 0
            else:
                cost = 1
            distance_matrix[i + 1][j + 1] = min(distance_matrix[i][j + 1] + 1,  # insert
                                                distance_matrix[i + 1][j] + 1,  # delete
                                                distance_matrix[i][j] + cost)  # replace
            if is_damerau:
                if i and j and word_1[i] == word_2[j - 1] and word_1[i - 1] == word_2[j]:
                    distance_matrix[i + 1][j + 1] = min(distance_matrix[i + 1][j + 1],
                                                        distance_matrix[i - 1][j - 1] + cost)  # transpose
    return distance_matrix


def get_string_oprations(word_1, word_2, is_damerau=True):
    dist_matrix = get_damerau_levenshtein_distance_matrix(word_1, word_2, is_damerau=is_damerau)
    i, j = len(dist_matrix), len(dist_matrix[0])
    i -= 1
    j -= 1
    operations_list = []
    while i != -1 and j != -1:
        if is_damerau and i > 1 and j > 1 and word_1[i - 1] == word_2[j - 2] and word_1[i - 2] \
                == word_2[j - 1]:
            if dist_matrix[i - 2][j - 2] < dist_matrix[i][j]:
                operations_list.insert(0, ('transpose', i - 1, i - 2))
                i -= 2
                j -= 2
                continue
        tmp = [dist_matrix[i - 1][j - 1], dist_matrix[i][j - 1], dist_matrix[i - 1][j]]
        index = tmp.index(min(tmp))
        if index == 0:
            if dist_matrix[i][j] > dist_matrix[i - 1][j - 1]:
                operations_list.insert(0, ('replace', i - 1, j - 1))
            i -= 1
            j -= 1
        elif index == 1:
            operations_list.insert(0, ('insert', i - 1, j - 1))
            j -= 1
        elif index == 2:
            operations_list.insert(0, ('delete', i - 1, i - 1))
            i -= 1
    return operations_list


class Distance:
    lev_thresholds = {'short_word': (4, 0.3), 'longer_words': (5, 0.6)}
    examples = {}

    def __init__(self, str_1, str_2, use_treshold: bool = False):
        # check condtitions to calculate Distances (thresholds for shorts and longer words)
        if (use_treshold and (((((len(str_1)) <= self.lev_thresholds['short_word'][0] or len(str_2)) <=
                                self.lev_thresholds['short_word'][0]) and
                               textdistance.damerau_levenshtein.normalized_similarity(str_1, str_2) >=
                               self.lev_thresholds['short_word'][1]) or
                              ((len(str_1)) >= self.lev_thresholds['longer_words'][0] and
                               textdistance.damerau_levenshtein.normalized_similarity(str_1, str_2) >=
                               self.lev_thresholds['longer_words'][1]))) or not use_treshold:
            print(str_1)
            self.string_1 = str_1
            self.template_string = str_2
            # self.operations = []
            # self.set_operations()

            # edit
            self.norm_sim_damerau_levenshtein = textdistance.damerau_levenshtein.normalized_similarity(self.string_1,
                                                                                                       self.template_string)
            self.damerau_levenshtein_distance = textdistance.damerau_levenshtein.distance(self.string_1,
                                                                                           self.template_string)

            self.norm_sim_jaro_winkler = textdistance.jaro_winkler.normalized_similarity(self.string_1, self.template_string)
            self.jaro_winkler_distance = textdistance.jaro_winkler.distance(self.string_1, self.template_string)
            # token based
            self.norm_sim_sorensen_dice = textdistance.sorensen_dice.normalized_similarity(self.string_1, self.template_string)
            self.sorensen_dice_distance = textdistance.sorensen_dice.distance(self.string_1, self.template_string)

            self.norm_sim_cosine = textdistance.cosine.normalized_similarity(self.string_1, self.template_string)
            self.cosine_distance = textdistance.cosine.distance(self.string_1, self.template_string)



            self.norm_sim_overlap = textdistance.overlap.normalized_similarity(self.string_1, self.template_string)
            self.overlap_distance = textdistance.overlap.distance(self.string_1, self.template_string)
            # phonetic
            self.norm_sim_mra = textdistance.mra.normalized_similarity(self.string_1, self.template_string)
            self.mra_distance = textdistance.mra.distance(self.string_1, self.template_string)

            # Sequence based
            self.norm_sim_lcsstr = textdistance.lcsstr.normalized_similarity(self.string_1, self.template_string)
            self.lcsstr_distance = textdistance.lcsstr.distance(self.string_1, self.template_string)

            self.norm_sim_gestalt = textdistance.ratcliff_obershelp.normalized_similarity(self.string_1, self.template_string)
            self.gestalt_distance = textdistance.ratcliff_obershelp.distance(self.string_1, self.template_string)

    def set_operations(self, is_damerau=True):
        for operation in get_string_oprations(self.string_1, self.template_string, is_damerau):
            if operation[0] == 'delete':
                self.operations.append(self.__set_operation_delete(operation))

            elif operation[0] == 'replace':
                self.operations.append(self.__set_operation_replace(operation))

            elif operation[0] == 'insert':
                self.operations.append(self.__set_operation_insert(operation))
            else:
                # e.g.
                self.operations.append(self.__set_operation_transpose(operation))

    def __set_operation_delete(self, operation: tuple):
        if operation[1] == 0 and operation[1] + 1 < len(self.string_1) - 1:
            return Delete(operation_subtype_id=1, deleted_char=self.string_1[operation[1]], idx=operation[1],
                          previous_char="", next_char=self.string_1[operation[1] + 1])

        # e.g.'haver', 'have' --> delete last char
        elif operation[1] == len(self.string_1) - 1:
            return Delete(operation_subtype_id=2, deleted_char=self.string_1[operation[1]], idx=operation[1],
                          previous_char=self.string_1[operation[1] - 1], next_char='')

        # e.g. 'harve', 'have' --> in the middle
        else:
            return Delete(operation_subtype_id=3, deleted_char=self.string_1[operation[1]], idx=operation[1],
                          previous_char=self.string_1[operation[1] - 1], next_char=self.string_1[operation[1] + 1])

    def __set_operation_replace(self, operation: tuple):
        if operation[1] - 1 >= 0 and operation[1] + 1 <= len(self.string_1) - 1:
            return Replace(operation_subtype_id=1, old_char=self.string_1[operation[1]],
                           new_char=self.template_string[operation[2]],
                           idx=operation[1],
                           previous_char=self.string_1[operation[1] - 1],
                           next_char=self.string_1[operation[1] + 1])
        elif operation[1] - 1 < 0 and operation[1] + 1 >= len(self.string_1) - 1:
            return Replace(operation_subtype_id=2, old_char=self.string_1[operation[1]],
                           new_char=self.template_string[operation[2]],
                           idx=operation[1],
                           previous_char='',
                           next_char='')
        elif operation[1] + 1 > len(self.string_1) - 1:
            return Replace(operation_subtype_id=3, old_char=self.string_1[operation[1]],
                           new_char=self.template_string[operation[2]],
                           idx=operation[1], previous_char=self.string_1[operation[1] - 1], next_char='')
        elif operation[1] - 1 < 0:
            return Replace(operation_subtype_id=4, old_char=self.string_1[operation[1]],
                           new_char=self.template_string[operation[2]],
                           idx=operation[1], previous_char='', next_char=self.string_1[operation[1] + 1])

    def __set_operation_transpose(self, operation):
        # left char is __word[operation[2]]
        # right char is __word[operation[2]]

        if operation[2] - 1 >= 0 and operation[1] + 1 <= len(self.string_1) - 1:
            return Transpose(operation_subtype_id=1, left_char=self.string_1[operation[2]], idx_left=operation[2],
                             right_char=self.string_1[operation[1]], idx_right=operation[1],
                             previous_char=self.string_1[operation[2] - 1],
                             next_char=self.string_1[operation[1] + 1])
        # e.g.
        elif operation[2] - 1 < 0 and operation[1] + 1 > len(self.string_1) - 1:
            return Transpose(operation_subtype_id=2, left_char=self.string_1[operation[2]], idx_left=operation[2],
                             right_char=self.string_1[operation[1]], idx_right=operation[1],
                             previous_char='', next_char='')
        # e.g.
        elif operation[1] + 1 > len(self.string_1) - 1:
            return Transpose(operation_subtype_id=3, left_char=self.string_1[operation[2]], idx_left=operation[2],
                             right_char=self.string_1[operation[1]], idx_right=operation[1],
                             previous_char=self.string_1[operation[2] - 1], next_char='')
        # e.g.
        elif operation[2] - 1 < 0:
            return Transpose(operation_subtype_id=4, left_char=self.string_1[operation[2]], idx_left=operation[2],
                             right_char=self.string_1[operation[1]], idx_right=operation[1],
                             previous_char="", next_char=self.string_1[operation[1] + 1])

    def __set_operation_insert(self, operation):
        # e.g.
        if operation[1] >= 0 and operation[1] + 1 <= len(self.string_1) - 1:
            return Insert(operation_subtype_id=1, new_char=self.template_string[operation[2]], idx=operation[1] + 1,
                          previous_char=self.string_1[operation[1]],
                          next_char=self.string_1[operation[1] + 1])
        # e.g.
        elif operation[1] < 0 and operation[1] + 1 > len(self.string_1) - 1:
            return Insert(operation_subtype_id=2, new_char=self.template_string[operation[2]], idx=operation[1] + 1,
                          previous_char='', next_char="")
        # e.g.
        elif operation[1] + 1 > len(self.string_1) - 1:
            return Insert(operation_subtype_id=3, new_char=self.template_string[operation[2]], idx=operation[1] + 1,
                          previous_char=self.string_1[operation[1]],
                          next_char='')
        # e.g.
        elif operation[1] < 0:
            return Insert(operation_subtype_id=4, new_char=self.template_string[operation[2]], idx=operation[1] + 1,
                          previous_char="",
                          next_char=self.string_1[operation[1] + 1])
