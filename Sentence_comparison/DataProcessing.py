import os.path
import time
import datetime
import objgraph
import pandas as pd
import psutil
from Sentence_comparison.Corrector import *
from Sentence_comparison.string_metrics import Distance
import json

def print_info(if_all=False):
    if if_all:
        print(3 * '\n')
        print('RAM memory % used:', psutil.virtual_memory()[2])
        print(objgraph.show_growth(limit=10))
    print('vars', vars())
    print('locals', locals())
    print('globals', globals())
    print('dir', dir())
    if if_all:
        print(3 * '\n')


def object_to_dicts(objct):
    if isinstance(objct, dict):
        return {k: object_to_dicts(v) for k, v in objct.items()}
    elif not isinstance(objct, str) and hasattr(objct, "__iter__"):
        return [object_to_dicts(v) for v in objct]
    elif hasattr(objct, "_ast"):
        return object_to_dicts(objct._ast())
    elif hasattr(objct, "__dict__"):
        return {
            key: object_to_dicts(value)
            for key, value in objct.__dict__.items()
            if not callable(value) and not key.startswith('_')
        }
    else:
        return objct


def verify_sentences(foo, template: str, test_sentence: str):
    start_time = time.time()
    dictionary = json.loads(
        json.dumps(Distance(str(foo(str(test_sentence))), str(template)), default=lambda o: o.__dict__))
    dictionary['time'] = time.time() - start_time
    df = pd.json_normalize(dictionary)
    del dictionary, start_time, test_sentence, template, foo
    return df


def save_pd_to_csv_file(dir_path: str, file_name: str,  df: pd.DataFrame):
    os.makedirs(os.path.normpath(dir_path), exist_ok=True)
    if not os.path.isfile(os.path.normpath(os.path.join(dir_path, file_name))) or os.stat(os.path.normpath(os.path.join(dir_path, file_name))).st_size == 0:
        df.to_csv((os.path.normpath(os.path.join(dir_path, file_name))), mode='w+', index=False, header=True)
    else:
        df.to_csv(os.path.normpath(os.path.join(dir_path, file_name)), mode='a', index=False, header=False)


def get_date():
    YEAR = str(datetime.date.today().year)  # the current year
    MONTH = str(datetime.date.today().month)  # the current month
    DATE = str(datetime.date.today().day)  # the current day
    HOUR = str(datetime.datetime.now().hour)  # the current hour
    MINUTE = str(datetime.datetime.now().minute)  # the current minute
    SECONDS = str(datetime.datetime.now().second)  # the current second
    return f'{YEAR}-{MONTH}-{DATE}\t{HOUR}:{MINUTE}:{SECONDS}'


def object_to_dicts(objct):
    if isinstance(objct, dict):
        return {k: object_to_dicts(v) for k, v in objct.items()}
    elif not isinstance(objct, str) and hasattr(objct, "__iter__"):
        return [object_to_dicts(v) for v in objct]
    elif hasattr(objct, "_ast"):
        return object_to_dicts(objct._ast())
    elif hasattr(objct, "__dict__"):
        return {
            key: object_to_dicts(value)
            for key, value in objct.__dict__.items()
            if not callable(value) and not key.startswith('_')
        }
    else:
        return objct


def read_json_file(path_to_file):
    with open(path_to_file, 'r') as f:
        data = json.load(f)
    return data


def write_object_to_json_file(path_to_file, key, main_dictionary):
    if os.path.isfile(path_to_file) and os.path.getsize(path_to_file) > 0:
        # open file
        data = read_json_file(path_to_file)
        # clear file
        open(path_to_file, 'w').close()
        # add data
        file = open(path_to_file, 'a+')
        data[key].append(main_dictionary)
        file.seek(0)
        json.dump(data, file, indent=4)
    else:
        file = open(path_to_file, 'w+')
        tmp = {key: [main_dictionary]}
        json.dump(tmp, file, indent=4)
    file.close()


def add_simple_dict_to_json_file(path_to_file, key, dict_obj):
    # check if is empty
    if os.path.isfile(path_to_file) and os.path.getsize(path_to_file) > 0:
        data = read_json_file(path_to_file)
        print(data)
        print(type(data['Sentence']))
        open(path_to_file, 'w').close()
        file = open(path_to_file, 'a+')
        if isinstance(dict_obj, dict) and dict_obj.keys():
            if key in data.keys():
                for k in dict_obj.keys():
                    if k not in data[key].keys():
                        data[key][k] = dict_obj[k]
                    elif k in data[key].keys() and (isinstance(data[key][k], int) or isinstance(data[key][k], float)):
                        data[key][k] += dict_obj[k]
            else:
                data[key] = dict_obj
        json.dump(data, file, indent=4)
        file.close()



# txt file cosntruction:
# (2*n+1) line --> grammarly correct
# 2*n line --> grammarly incorrect (could be empty)

# x = True
# while x:
#     try:
#         for k in os.listdir(directory):
#             i = 0
#             with open(directory + '\\' + k) as file:
#                 while i < 50:
#                     correct_sentence = file.readline()
#                     wrong_grammar_sentence = file.readline()
#                     start = time.time()
#                     correct_sentence = findall(r'[^\n]+', correct_sentence)[0]
#                     if len(wrong_grammar_sentence) > 1:
#                         wrong_grammar_sentence = findall(r'[^\n]+', wrong_grammar_sentence)[0]
#                     misspells = [misspell_sentence(correct_sentence, k) for k in range(1, 5)]
#
#                     verify_sentences(correct_spelling_spell_checker, correct_sentence, correct_sentence,
#                                      'spellchecker\\false_positives.csv')
#                     if len(wrong_grammar_sentence) > 1:
#                         verify_sentences(correct_spelling_spell_checker, correct_sentence, wrong_grammar_sentence,
#                                          'spellchecker\\true_positives.csv')
#                     verify_sentences(correct_spelling_spell_checker, correct_sentence, misspells[0],
#                                      'spellchecker\\one_misspell.csv')
#                     verify_sentences(correct_spelling_spell_checker, correct_sentence, misspells[1],
#                                      'spellchecker\\two_misspells.csv')
#                     verify_sentences(correct_spelling_spell_checker, correct_sentence, misspells[2],
#                                      'spellchecker\\three_misspells.csv')
#                     verify_sentences(correct_spelling_spell_checker, correct_sentence, misspells[3],
#                                      'spellchecker\\four_misspells.csv')
#
#                     # verify_sentences(correct_spelling_txt_blb, correct_sentence, correct_sentence,
#                     #                  'textblob\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(correct_spelling_txt_blb, correct_sentence, wrong_grammar_sentence,
#                     #                      'textblob\\true_positives.csv')
#                     # verify_sentences(correct_spelling_txt_blb, correct_sentence, misspells[0],
#                     #                  'textblob\\one_misspell.csv')
#                     # verify_sentences(correct_spelling_txt_blb, correct_sentence, misspells[1],
#                     #                  'textblob\\two_misspells.csv')
#                     # verify_sentences(correct_spelling_txt_blb, correct_sentence, misspells[2],
#                     #                  'textblob\\three_misspells.csv')
#                     # verify_sentences(correct_spelling_txt_blb, correct_sentence, misspells[3],
#                     #                  'textblob\\four_misspells.csv')
#                     #
#                     # verify_sentences(correct_spelling_autocorrect, correct_sentence, correct_sentence,
#                     #                  'autocorrect\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(correct_spelling_autocorrect, correct_sentence, wrong_grammar_sentence,
#                     #                      'autocorrect\\true_positives.csv')
#                     # verify_sentences(correct_spelling_autocorrect, correct_sentence, misspells[0],
#                     #                  'autocorrect\\one_misspell.csv')
#                     # verify_sentences(correct_spelling_autocorrect, correct_sentence, misspells[1],
#                     #                  'autocorrect\\two_misspells.csv')
#                     # verify_sentences(correct_spelling_autocorrect, correct_sentence, misspells[2],
#                     #                  'autocorrect\\three_misspellscsv')
#                     # verify_sentences(correct_spelling_autocorrect, correct_sentence, misspells[3],
#                     #                  'autocorrect\\four_misspells.csv')
#
#                     # verify_sentences(grammar_check_gingerit, correct_sentence, correct_sentence,
#                     #                  'gingerit\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_gingerit, correct_sentence, wrong_grammar_sentence,
#                     #                      'gingerit\\true_positives.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence, misspells[0],
#                     #                  'gingerit\\one_misspell.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence, misspells[1],
#                     #                  'gingerit\\two_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence, misspells[2],
#                     #                  'gingerit\\three_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence, misspells[3],
#                     #                  'gingerit\\four_misspells.csv')
#                     #
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_spell_checker(correct_sentence),
#                     #                  'gingerit_spellchecker\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                      correct_spelling_spell_checker(wrong_grammar_sentence),
#                     #                      'gingerit_spellchecker\\true_positives.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[0]),
#                     #                  'gingerit_spellchecker\\one_misspell.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[1]),
#                     #                  'gingerit_spellchecker\\two_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[2]),
#                     #                  'gingerit_spellchecker\\three_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[3]),
#                     #                  'gingerit_spellchecker\\four_misspells.csv')
#
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_txt_blb(correct_sentence),
#                     #                  'gingerit_textblob\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                      correct_spelling_txt_blb(wrong_grammar_sentence),
#                     #                      'gingerit_textblob\\true_positives.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[0]),
#                     #                  'gingerit_textblob\\one_misspell.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[1]),
#                     #                  'gingerit_textblob\\two_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[2]),
#                     #                  'gingerit_textblob\\three_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[3]),
#                     #                  'gingerit_textblob\\four_misspells.csv')
#                     # # #
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_autocorrect(correct_sentence),
#                     #                  'gingerit_autocorrect\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                      correct_spelling_autocorrect(wrong_grammar_sentence),
#                     #                      'gingerit_autocorrect\\true_positives.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,correct_spelling_autocorrect(misspells[0]),
#                     #                  'gingerit_autocorrect\\one_misspell.csv'), correct_spelling_autocorrect(misspells[1]),
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[1]),
#                     #                  'gingerit_autocorrect\\two_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[2]),
#                     #                  'gingerit_autocorrect\\three_misspells.csv')
#                     # verify_sentences(grammar_check_gingerit, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[3]),
#                     #                  'gingerit_autocorrect\\four_misspells.csv')
#
#
#                     # verify_sentences(grammar_check_language_tool, correct_sentence, correct_sentence,
#                     #                  'language_tool\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_language_tool, correct_sentence, wrong_grammar_sentence,
#                     #                      'language_tool\\true_positives.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence, misspells[0],
#                     #                  'language_tool\\one_misspell.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence, misspells[1],
#                     #                  'language_tool\\two_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence, misspells[2],
#                     #                  'language_tool\\three_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence, misspells[3],
#                     #                  'language_tool\\four_misspells.csv')
#                     #
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_spell_checker(correct_sentence),
#                     #                  'language_tool_spellchecker\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                      correct_spelling_spell_checker(wrong_grammar_sentence),
#                     #                      'language_tool_spellchecker\\true_positives.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[0]),
#                     #                  'language_tool_spellchecker\\one_misspell.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[1]),
#                     #                  'language_tool_spellchecker\\two_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[2]),
#                     #                  'language_tool_spellchecker\\three_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_spell_checker(misspells[3]),
#                     #                  'language_tool_spellchecker\\four_misspells.csv')
#                     #
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_txt_blb(correct_sentence),
#                     #                  'language_tool_textblob\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                      correct_spelling_txt_blb(wrong_grammar_sentence),
#                     #                      'language_tool_textblob\\true_positives.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[0]),
#                     #                  'language_tool_textblob\\one_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[1]),
#                     #                  'language_tool_textblob\\two_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[2]),
#                     #                  'language_tool_textblob\\three_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_txt_blb(misspells[3]),
#                     #                  'language_tool_textblob\\four_misspells.csv')
#                     #
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_autocorrect(correct_sentence),
#                     #                  'language_tool_autocorrect\\false_positives.csv')
#                     # if len(wrong_grammar_sentence) > 1:
#                     #     verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                      correct_spelling_autocorrect(wrong_grammar_sentence),
#                     #                      'language_tool_autocorrect\\true_positives.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[0]),
#                     #                  'language_tool_autocorrect\\one_misspell.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[1]),
#                     #                  'language_tool_autocorrect\\two_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[2]),
#                     #                  'language_tool_autocorrect\\three_misspells.csv')
#                     # verify_sentences(grammar_check_language_tool, correct_sentence,
#                     #                  correct_spelling_autocorrect(misspells[3]),
#                     #                  'language_tool_autocorrect\\four_misspells.csv')
#                     i += 1
#                     print_info(True)
#                     gc.collect()
#                     del correct_sentence, wrong_grammar_sentence
#                     print_info(True)
#         x = False
#
#     except Exception as exc:
#         pass
#     # finally: x = False
#     # with open('results\\logs.txt', mode='a+') as log_file:
#     #     log_file.write(str(get_date()) + '\t' + str(exc))
#     #     log_file.write(str(exc.args))
#     #     log_file.write(str('\n'))

# finally: pass
