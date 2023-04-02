# %%  upload libraries and load data
import matplotlib.ticker as ticker
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from graphs import get_hist_board, config_plot_for_latex

df = pd.read_csv("./csv_output/fp.csv", delimiter=';')

# rename column names

col_name_map = {
    'string_1': 'Tested string',
    'template_string': 'Template string',
    'norm_sim_damerau_levenshtein': 'Damerau–Levenshtein normalized similarity ',
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
    'time': 'Time'
}

df.rename(columns=col_name_map, inplace=True)
df.sort_values(by='function', inplace=True)
df['function'] = df["function"].astype("category")
# drop non-number columns
df = df.select_dtypes(exclude=['object'])
# %%  create histograms


# chunk df by function
chunk_size = 7
function_chunks = [list(df['function'].unique())[i * chunk_size:(i + 1) * chunk_size] for i in
                   range((len(list(df['function'].unique())) + chunk_size - 1) // chunk_size)]
df['function'] = df["function"].astype("object")


config_plot_for_latex()
for col in [c for c in df.columns if c != 'function']:
    get_hist_board(df, function_chunks, col, by='function', title=f"False positives {col}",
                   bins=10, file_path = f'./plots/review/hist/fp_{col}.pgf')


# %%  create histograms


def hexbin(x, y, color, **kwargs):
    cmap = sns.light_palette(color, as_cmap=True)
    plt.hexbin(x, y, gridsize=15, cmap=cmap, **kwargs)
