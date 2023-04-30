import pandas as pd

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
    'function': 'Function',
    'time': 'Time',
    'sentence_before_corr': "Sentence before correction",
    'operations_made_to_create_misspells': "Operations made to create misspells",
    'amount_of_errors': "Amount of misspells (in input sentence)"
}

total_results_df = {'EDIT': pd.DataFrame(), 'PHONETIC': pd.DataFrame(), 'TOKEN': pd.DataFrame(),
                    'SEQUENCE': pd.DataFrame()}

TYPES_COLUMN_NAMES = {
    'EDIT': [
        # 'Damerau–Levenshtein normalized similarity',
        'Damerau–Levenshtein distance',
        'Jaro-Winkler normalized similarity',
        # 'Jaro-Winkler distance'
    ],
    'PHONETIC': [
        'Match rating approach normalized similarity',
        # 'Match rating approach distance'
    ],

    'TOKEN': [
        #'Sørensen–Dice coefficient (normalized similarity)',
        'Sørensen–Dice coefficient ',
        #'Cosine normalized similarity',
        'Cosine distance',
        'Szymkiewicz–Simpson coefficient (normalized similarity)',
        #'Szymkiewicz–Simpson coefficient'
    ],
    'SEQUENCE': [
        'Longest common substring similarity (normalized similarity)',
        # 'Longest common substring similarity distance',
        'Ratcliff-Obershelp similarity (normalized similarity)',
        # 'Ratcliff-Obershelp similarity (distance)'
    ],
    # 'INFO': ['Function', 'Amount of misspells (in input sentence)', 'Time']
}


def categorize_by_quantile(x, goal, quantiles: list, values:list,  ascending_is_better: bool = True):
    """Ascending_is_better is True if the goal THE HIGHEST value (e.g. similarity), False otherwise."""
    if len(values) < 4: 
        for i in range(4):
            values.append(None)
    if ascending_is_better:
        if  x == goal:
            return values[0]
        elif goal > x >= quantiles[2]:
            return values[1]
        elif quantiles[2] > x >= quantiles[1]: 
            return values[2]
        else: return  values[3]
    else: 
        if  x == goal:
            return values[0]
        elif goal < x <= quantiles[0]:
            return values[1]
        elif quantiles[1] >= x > quantiles[0]: 
            return values[2]
        else: return values[3]
        
