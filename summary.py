import pandas as pd
import matplotlib as plt
import seaborn as sns
rand_df = pd.read_csv("./csv_output/rand_misspells.csv", delimiter=';')
key_missp_df = pd.read_csv("./csv_output/key_misspells.csv", delimiter=';')
fp_df = pd.read_csv("./csv_output/fp.csv", delimiter=';')
col_name_map = {
    'string_1': 'Tested string',
    'template_string': 'Template string',
    'norm_sim_damerau_levenshtein': 'Damerau–Levenshtein normalized similarity',
    'damerau_levenshtein_distance': 'Damerau–Levenshtein distance',
    'norm_sim_jaro_winkler': 'Jaro-Winkler normalized similarity',
    'jaro_winkler_distance': 'Jaro-Winkler distance',
    'norm_sim_sorensen_dice': 'Sørensen–Dice coefficient (normalized similarity)',
    'sorensen_dice_distance': 'Sørensen–Dice coefficient ',
    'norm_sim_cosine': 'Cosine normalized similarity',
    'cosine_distance': 'Cosine distance',
    'norm_sim_overlap': 'Szymkiewicz–Simpson coefficient (normalized similarity)',
    'overlap_distance': 'Szymkiewicz–Simpson coefficient',
    'norm_sim_mra': 'Match rating approach normalized similarity',
    'mra_distance': 'Match rating approach distance',
    'norm_sim_lcsstr': 'Longest common substring similarity (normalized similarity)',
    'lcsstr_distance': 'Longest common substring similarity distance',
    'norm_sim_gestalt': 'Ratcliff-Obershelp similarity (normalized similarity)',
    'gestalt_distance': 'Ratcliff-Obershelp similarity (distance)',
    'function': 'function',
    'time': 'Time',
    'sentence_before_corr': "Sentence before correction",
    'operations_made_to_create_misspells': "Operations made to create misspells",
    'amount_of_errors': "Amount of misspells (in input sentence)"
}
rand_df.rename(columns=col_name_map, inplace=True)
key_missp_df.rename(columns=col_name_map, inplace=True)
fp_df.rename(columns=col_name_map, inplace=True)

# %% write to file summary
"""
# description = rand_df.groupby(by=['function', "Amount of misspells (in input sentence)"]).describe()
# description = key_missp_df.groupby(by=['function', "Amount of misspells (in input sentence)"]).describe()
description = fp_df.groupby(by=['function']).describe()

cols_to_drop = []
i = 0
for k in description.columns:
    if 'count' in k and i >= 1:
        cols_to_drop.append(k)
    elif 'count' in k: print(k)
    i += 1

print(len(description.columns))
description.drop(cols_to_drop, axis=1, inplace=True)

# description.to_csv('./plots/description_rand_df.csv', mode='w+')
# description.to_csv('./plots/description_key_missp_df.csv', mode='w+')
description.to_csv('./plots/description_fp_df.csv', mode='w+')
"""
# %%


