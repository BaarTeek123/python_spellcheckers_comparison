from Sentence_Generator.MisspellGenerator import misspell_sentence
from Sentence_comparison.Corrector import correct_with_autocorrect, correct_with_spellchecker, correct_with_textblob
from Sentence_comparison.Corrector import correct_with_gingerit, correct_with_languagetool, correct_with_gramformer, \
    correct_with_jamspell
import pandas as pd
import os

from Sentence_comparison.DataProcessing import object_to_dicts
from Sentence_comparison.string_metrics import Distance


def run_list_of_functions(list_of_funcs, sentence):
    time = 0
    for fun in list_of_funcs:
        sentence, tmp = fun(sentence)
        time += tmp
    return sentence, time


def append_to_csv(data: dict, path_to_file: str, **kwargs):
    path_to_file = os.path.normpath(path_to_file)
    if os.path.exists(path_to_file) and os.stat(path_to_file).st_size == 0 or not os.path.exists(path_to_file):
        pd.DataFrame([data]).to_csv(path_to_file, mode='w+', index=False, **kwargs)

        return
    pd.DataFrame([data]).to_csv(path_to_file, header=False, mode='a', index=False, **kwargs)


list_of_functions = {'Autocorrect': [correct_with_autocorrect],
                     'SpellChecker': [correct_with_spellchecker],
                     'TextBlob': [correct_with_textblob],
                     'Gingerit': [correct_with_gingerit],
                     'LanguageTool': [correct_with_languagetool],
                     "GramFormer": [correct_with_gramformer],
                     "Jamspell": [correct_with_jamspell],
                     "Autocorrect(SpellChecker)": [correct_with_autocorrect, correct_with_spellchecker],
                     "Autocorrect(TextBlob)": [correct_with_autocorrect, correct_with_textblob],
                     "Autocorrect(Gingerit)": [correct_with_autocorrect, correct_with_gingerit],
                     "Autocorrect(LanguageTool)": [correct_with_autocorrect, correct_with_languagetool],
                     "Autocorrect(GramFormer)": [correct_with_autocorrect, correct_with_gramformer],
                     "Autocorrect(Jamspell)": [correct_with_autocorrect, correct_with_jamspell],
                     "SpellChecker(Autocorrect)": [correct_with_spellchecker, correct_with_autocorrect],
                     "SpellChecker(TextBlob)": [correct_with_spellchecker, correct_with_textblob],
                     "SpellChecker(Gingerit)": [correct_with_spellchecker, correct_with_gingerit],
                     "SpellChecker(LanguageTool)": [correct_with_spellchecker, correct_with_languagetool],
                     "SpellChecker(GramFormer)": [correct_with_spellchecker, correct_with_gramformer],
                     "SpellChecker(Jamspell)": [correct_with_spellchecker, correct_with_jamspell],
                     "TextBlob(Autocorrect)": [correct_with_textblob, correct_with_autocorrect],
                     "TextBlob(SpellChecker)": [correct_with_textblob, correct_with_spellchecker],
                     "TextBlob(Gingerit)": [correct_with_textblob, correct_with_gingerit],
                     "TextBlob(LanguageTool)": [correct_with_textblob, correct_with_languagetool],
                     "TextBlob(GramFormer)": [correct_with_textblob, correct_with_gramformer],
                     "TextBlob(Jamspell)": [correct_with_textblob, correct_with_jamspell],
                     "Gingerit(Autocorrect)": [correct_with_gingerit, correct_with_autocorrect],
                     "Gingerit(SpellChecker)": [correct_with_gingerit, correct_with_spellchecker],
                     "Gingerit(TextBlob)": [correct_with_gingerit, correct_with_textblob],
                     "Gingerit(LanguageTool)": [correct_with_gingerit, correct_with_languagetool],
                     "Gingerit(GramFormer)": [correct_with_gingerit, correct_with_gramformer],
                     "Gingerit(Jamspell)": [correct_with_gingerit, correct_with_jamspell],
                     "LanguageTool(Autocorrect)": [correct_with_languagetool, correct_with_autocorrect],
                     "LanguageTool(SpellChecker)": [correct_with_languagetool, correct_with_spellchecker],
                     "LanguageTool(TextBlob)": [correct_with_languagetool, correct_with_textblob],
                     "LanguageTool(Gingerit)": [correct_with_languagetool, correct_with_gingerit],
                     "LanguageTool(GramFormer)": [correct_with_languagetool, correct_with_gramformer],
                     "LanguageTool(Jamspell)": [correct_with_languagetool, correct_with_jamspell],
                     "GramFormer(Autocorrect)": [correct_with_gramformer, correct_with_autocorrect],
                     "GramFormer(SpellChecker)": [correct_with_gramformer, correct_with_spellchecker],
                     "GramFormer(TextBlob)": [correct_with_gramformer, correct_with_textblob],
                     "GramFormer(Gingerit)": [correct_with_gramformer, correct_with_gingerit],
                     "GramFormer(LanguageTool)": [correct_with_gramformer, correct_with_languagetool],
                     "GramFormer(Jamspell)": [correct_with_gramformer, correct_with_jamspell],
                     "Jamspell(Autocorrect)": [correct_with_jamspell, correct_with_autocorrect],
                     "Jamspell(SpellChecker)": [correct_with_jamspell, correct_with_spellchecker],
                     "Jamspell(TextBlob)": [correct_with_jamspell, correct_with_textblob],
                     "Jamspell(Gingerit)": [correct_with_jamspell, correct_with_gingerit],
                     "Jamspell(LanguageTool)": [correct_with_jamspell, correct_with_languagetool],
                     "Jamspell(GramFormer)": [correct_with_jamspell, correct_with_gramformer]}

if __name__ == '__main__':
    sentences = open("./texts/input_sentences.txt").read().split('\n')
    sentences = [sent for sent in sentences if len(sent.split()) <= 6][4500:5000]
    for template in sentences:
        i = 1
        while i <= 8:
            keys_misspelled, key_ops = misspell_sentence(template, i, False)
            random_misspelled, random_ops = misspell_sentence(template, i, True)

            # choose only element from 0 idx - functions return a tuple (output, corrected string, time)
            for name, fun in list_of_functions.items():
                if i == 1:
                    # fp, fp_time = fun[0](fun[1](template)[0])  # detect false positives
                    fp, fp_time = run_list_of_functions(fun, template)
                    dictionary = object_to_dicts(Distance(fp, template))
                    dictionary['function'] = name
                    dictionary['time'] = fp_time
                    append_to_csv(dictionary, f'./csv_output/fp.csv', sep=';')

                    # if os.stat('collection1.dat').st_size == 0:

                    # pd.DataFrame.from_dict(dictionary).to_csv(file_path,mode='a+', index=False, sep=';')
                # detect key positives
                key_corrected_sentence, key_correction_time = run_list_of_functions(fun, keys_misspelled)
                # detect random positives
                rand_corrected_sentence, rand_correction_time = run_list_of_functions(fun, random_misspelled)
                # file_path = os.path.abspath (f'./csv_output/{name.lower()}')
                # os.makedirs(file_path, exist_ok=True)

                # distances between key corrected and template to dict
                dictionary = object_to_dicts(Distance(key_corrected_sentence, template))
                # add additional fields
                dictionary['sentence_before_corr'] = keys_misspelled
                dictionary['operations_made_to_create_misspells'] = str(key_ops)
                dictionary['function'] = name
                dictionary['amount_of_errors'] = i
                dictionary['time'] = key_correction_time
                # distances between key corrected and template to csv
                append_to_csv(dictionary, f'./csv_output/key_misspells.csv', sep=';')
                # pd.DataFrame(dictionary).to_csv(os.path.normpath(f'./csv_output/{i}key_misspells.csv'),
                #                                 mode='a+', sep=';')

                # distances between rand corrected and template to dict
                dictionary = object_to_dicts(Distance(rand_corrected_sentence, template))
                # add additional fields
                dictionary['sentence_before_corr'] = random_misspelled
                dictionary['operations_made_to_create_misspells'] = str(random_ops)
                dictionary['function'] = name
                dictionary['amount_of_errors'] = i
                dictionary['time'] = rand_correction_time
                # distances between rand corrected and template to csv
                append_to_csv(dictionary, f'./csv_output/rand_misspells.csv', sep=';')
            if i < 5:
                i+=1
            else:
                i+=2



