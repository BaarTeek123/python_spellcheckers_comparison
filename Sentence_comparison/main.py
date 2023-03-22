"""
import os.path
from Sentence_Generator.MisspellGenerator import misspell_sentence
from Sentence_comparison.DataProcessing import *
from Sentence_comparison.Comparer import *

list_of_functions = {'Autocorrect': correct_with_autocorrect, 'SpellChecker': correct_with_spellchecker,
                     'TextBlob': correct_with_textblob, 'Gingerit': correct_with_gingerit,
                     'LanguageTool': correct_with_languagetool, "GramFormer": correct_with_gramformer}

# nordvpn_switcher.initialize_VPN(save=1, area_input=None, skip_settings=None)
#     # nordvpn_switcher.rotate_VPN()
#     directory = os.path.normpath(os.path.abspath('..') + '/' + 'Sentences')  # directory with .txt files
#     result_dir = "../Results/"
#     it, amount_of_sentences_from_one_txt_file = 0, 50
#     amount_of_misspells = 6
#     for sub_dir in os.listdir(os.path.normpath(directory)):
#         for file_dir in os.listdir(os.path.normpath(directory + '/' + sub_dir)):
#             print(file_dir)
#             # read files
#             with open(os.path.normpath(directory + '/' + sub_dir + '/' + file_dir)) as file:
#                 while it < amount_of_sentences_from_one_txt_file:
#                     correct_sentence = file.readline().replace('\n', '')
#                     wrong_grammar_sentence = file.readline().replace('\n', '')
#                     # misspell correct sentences
#                     misspells_from_correct_sentence = [misspell_sentence(correct_sentence, k)[0] for k in
#                                                        range(1, amount_of_misspells)]
#                     # list of lists of misspells types
#                     misspells_operations_correct_sentence = [misspell_sentence(correct_sentence, k)[1] for k in
#                                                              range(1, amount_of_misspells)]
#                     # save false positives
#                     for fun_name in list_of_functions.keys():
#                         save_pd_to_csv_file(f'{result_dir}{fun_name}', 'false_positives.csv',
#                                             verify_sentences(list_of_functions[fun_name], template=correct_sentence,
#                                                              test_sentence=correct_sentence))
#                     # misspell grammar correct sentences
#                     for i in range(len(misspells_from_correct_sentence)):
#                         for fun_name in list_of_functions.keys():
#                             df = pd.concat([verify_sentences(list_of_functions[fun_name], template=correct_sentence,
#                                                              test_sentence=misspells_from_correct_sentence[i]),
#                                             pd.DataFrame(misspells_operations_correct_sentence[i], index=[0])], axis=1)
#                             save_pd_to_csv_file(f'{result_dir}{fun_name}', str(i + 1) + '_correct_misspelled.csv', df)
#
#                     # use grammar incorrect sentences if exists
#                     if len(wrong_grammar_sentence) > 1:
#                         for fun_name in list_of_functions.keys():
#                             save_pd_to_csv_file(f'{result_dir}{fun_name}', 'grammar.csv',
#                                                 verify_sentences(list_of_functions[fun_name], template=correct_sentence,
#                                                                  test_sentence=wrong_grammar_sentence))
#
#                         misspelled_sentence_from_grammar_incorrect = [misspell_sentence(wrong_grammar_sentence, k)[0]
#                                                                       for k in range(1, amount_of_misspells)]
#                         misspells_operations_grammar_incorrect_sentence = [
#                             misspell_sentence(wrong_grammar_sentence, k)[1] for k in range(1, amount_of_misspells)]
#                         # misspell grammar incorrect sentences
#                         for i in range(len(misspelled_sentence_from_grammar_incorrect)):
#                             for fun_name in list_of_functions.keys():
#                                 df = pd.concat([verify_sentences(list_of_functions[fun_name], template=correct_sentence,
#                                                                  test_sentence= misspelled_sentence_from_grammar_incorrect[i]),
#                                                 pd.DataFrame(misspells_operations_grammar_incorrect_sentence[i],
#                                                              index=[0])], axis=1)
#                                 save_pd_to_csv_file(f'{result_dir}{fun_name}', str(i + 1) + '_incorrect_misspelled.csv', df)
#
#                     it += 1
#                     print(it)

import gramformer
from Comparer import correct_with_gramformer

# # spacy.cli.download("en_core_web_md")
# gramformer_tool = gramformer.Gramformer(models=1)
# sentence = "I loves this shit."
# print("Correct: ", correct_with_gramformer(sentence))

from pygrammalecte import grammalecte_text
texte_bidon = "I really like this piece of shit"


for message in grammalecte_text(texte_bidon):
    print(message)
"""


from Sentence_comparison.Corrector import *

list_of_functions = {'Autocorrect': correct_with_autocorrect,
                     'SpellChecker': correct_with_spellchecker,
                     'TextBlob': correct_with_textblob,
                     'Gingerit': correct_with_gingerit,
                     'LanguageTool': correct_with_languagetool,
                     "GramFormer": correct_with_gramformer,
                     "Jamspell": correct_with_jamspell,
                     "NeuSpell": correct_with_neuspell}


if __name__ == '__main__':
    sentences = open("./texts/input_sentences.txt").read().split('\n')[:100]
    print(sentences)