# %%  upload libraries and load data
from itertools import chain
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from data_analysis_config import col_name_map


# load dataframe
fp_df = pd.read_csv("./csv_output/fp.csv", delimiter=';')
key_df = pd.read_csv("./csv_output/key_misspells.csv", delimiter=';')
rand_df = pd.read_csv("./csv_output/rand_misspells.csv", delimiter=';')

fp_df['amount_of_errors'] = 0

# rename dataframe
fp_df.rename(columns=col_name_map, inplace=True)
key_df.rename(columns=col_name_map, inplace=True)
rand_df.rename(columns=col_name_map, inplace=True)

fp_df['Function'] = fp_df["Function"].astype("category")
key_df['Function'] = key_df["Function"].astype("category")
rand_df['Function'] = rand_df["Function"].astype("category")

# delete strings
fp_df = fp_df.select_dtypes(exclude=['object'])
key_df = key_df.select_dtypes(exclude=['object'])
rand_df = rand_df.select_dtypes(exclude=['object'])

fp_df['Function'] = fp_df["Function"].astype("object")
key_df['Function'] = key_df["Function"].astype("object")
rand_df['Function'] = rand_df["Function"].astype("object")

data_frames = {"False positive": fp_df, "Misspells based on keyboard QWERTY [0-5] u {7}": key_df,
               "Random misspells [0-5] u {7}": rand_df}
for k in key_df["Amount of misspells (in input sentence)"].unique():
    data_frames[f'{k} misspells based on QWERTY keyboard in input sentence'] = key_df[
        key_df["Amount of misspells (in input sentence)"] == k].reset_index()
for k in rand_df["Amount of misspells (in input sentence)"].unique():
    data_frames[f'{k} random misspells in input sentence'] = rand_df[
        rand_df["Amount of misspells (in input sentence)"] == k].reset_index()

# %% define weights

# weights for 1, 2, 3 rd range
WEIGTHS = [1, 0.35, 0.15]

# points for classification
POINTS = [20, 16, 13, 10, 7, 5, 4, 3, 2, 1]

total_results_df = {'EDIT': pd.DataFrame(), 'PHONETIC': pd.DataFrame(), 'TOKEN': pd.DataFrame(),
                    'SEQUENCE': pd.DataFrame()}
RESULT_COLUMN_NAMES = ['Full correctness', 'First range', 'Second range']
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
        # 'Sørensen–Dice coefficient (normalized similarity)',
        'Sørensen–Dice coefficient ',
        # 'Cosine normalized similarity',
        'Cosine distance',
        'Szymkiewicz–Simpson coefficient (normalized similarity)',
        # 'Szymkiewicz–Simpson coefficient'
    ],
    'SEQUENCE': [
        'Longest common substring similarity (normalized similarity)',
        # 'Longest common substring similarity distance',
        'Ratcliff-Obershelp similarity (normalized similarity)',
        # 'Ratcliff-Obershelp similarity (distance)'
    ],
    # 'INFO': ['Function', 'Amount of misspells (in input sentence)', 'Time']
}

# %% create classification
for by in list(chain.from_iterable(TYPES_COLUMN_NAMES.values())):
    for name, combined in data_frames.items():
        # assign quantile and median
        if 'QWERTY'.lower() in name.lower():
            quantiles = [key_df[by].quantile(0.25), key_df[by].quantile(
                0.5), key_df[by].quantile(0.75)]
        elif 'random'.lower() in name.lower():
            quantiles = [rand_df[by].quantile(0.25), rand_df[by].quantile(
                0.5), rand_df[by].quantile(0.75)]
        else:
            quantiles = [fp_df[by].quantile(0.25), fp_df[by].quantile(
                0.5), fp_df[by].quantile(0.75)]
        # normalized similarity
        if 'normalized similarity'.lower() in by.lower():
            # goal for similarity
            goal = 1.0

            # 1st is full correctness between the corrected and the template
            # 2nd is between goal and 3rd quantile
            # 3rd is 3rd quantile and 2nd quantile
            scores = combined.groupby('Function')[by].agg(
                [(RESULT_COLUMN_NAMES[0], lambda x: (x == goal).sum()),
                 (RESULT_COLUMN_NAMES[1], lambda x: (
                     (x < goal) & (x >= quantiles[2])).sum()),
                 (RESULT_COLUMN_NAMES[2], lambda x: (
                     (x >= quantiles[1]) & (x < quantiles[2])).sum()),
                 ('Total count', 'count')])

        # distance
        else:
            # goal for distances
            goal = 0.0

            # 1st is full correctness between the corrected and the template
            # 2nd is between goal and 1st quantile
            # 3rd is 1st quantile and 2nd quantile
            scores = combined.groupby('Function')[by].agg(
                [(RESULT_COLUMN_NAMES[0], lambda x: (x == goal).sum()),
                 (RESULT_COLUMN_NAMES[1], lambda x: (
                     (x > goal) & (x <= quantiles[0])).sum()),
                 (RESULT_COLUMN_NAMES[2], lambda x: (
                     (x > quantiles[0]) & (x <= quantiles[1])).sum()),
                 ('Total count', 'count')])

        # normalize results to the count of function
        for col_name in RESULT_COLUMN_NAMES:
            scores[col_name] = scores[col_name] / scores['Total count']

        # calculate weighted average of first, second and the third range
        scores['Weighted average'] = scores[RESULT_COLUMN_NAMES].dot(WEIGTHS)
        scores.sort_values(by='Weighted average',
                           ascending=False, inplace=True)

        # assign default classification and score value
        scores['Classification'] = 'Not in top 10'
        scores['Score'] = 0
        # assign values for classification for top 10
        scores.loc[scores['Weighted average'].nlargest(
            10).index, 'Classification'] = 'Top 10'
        scores.loc[scores['Weighted average'].nlargest(
            10).index, 'Score'] = POINTS
        VARIANT = next(
            (key for key, values in TYPES_COLUMN_NAMES.items() if by in values), None)
        total_results_df[VARIANT] = pd.concat(
            [total_results_df[VARIANT], scores], axis=1)


for k in total_results_df.keys():
    total_results_df[k]['Total'] = total_results_df[k]['Score'].sum(axis=1)
    total_results_df[k].sort_values(by='Total', ascending=False, inplace=True)
    print(k, total_results_df[k].shape)
    # total_results_df[k]['Total'] = pd.concat([val['Score'] for val in total_results_df.values()], axis=1).sum(axis=1)
    # total_results_df[k].sort_values(by='Total', ascending=False, inplace=True)

# with pd.ExcelWriter("output.xlsx", mode="w+") as f:
#     for k in total_results_df.keys():
#         total_results_df[k].to_excel(f, sheet_name=k)
#
#
#
# concat_scores = pd.concat([val['Total'] for val in total_results_df.values()], axis=1).sum(axis=1).sort_values(ascending=False)
# with pd.ExcelWriter("output.xlsx", mode="a") as f:
#     concat_scores.to_excel(f, sheet_name='Summary')


# f = suma (clasyfikacji_1*waga)
