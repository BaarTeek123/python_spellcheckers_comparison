# %%  upload libraries and load data
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from graphs import config_plot_for_latex
import plotly.graph_objects as go

df = pd.read_csv("./csv_output/rand_misspells.csv", delimiter=';')
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
df.rename(columns=col_name_map, inplace=True)
df.sort_values(by='function', inplace=True)
df['function'] = df["function"].astype("category")
# drop non-number columns
df = df.select_dtypes(exclude=['object'])
df['function'] = df["function"].astype("object")

# %%  upload libraries and load data
chunk_size=7
function_chunks = [list(df['function'].unique())[i * chunk_size:(i + 1) * chunk_size] for i in
                   range((len(list(df['function'].unique())) + chunk_size - 1) // chunk_size)]
# upper = key_miss_df[key_miss_df['function'].isin(function_chunks[0][:4]) == True].reset_index(drop=True)
# lower = key_miss_df[key_miss_df['function'].isin(function_chunks[0][4:]) == True].reset_index(drop=True)


# ax = sns.swarmplot(data=df[df['function'].isin(function_chunks[0])], x="Damerau–Levenshtein normalized similarity", y="Amount of misspells (in input sentence)", hue="function")
# ax.set(ylabel="")

# %%  draw distplot

# config_plot_for_latex()
# for col in [c for c in df.columns if c not in ["Amount of misspells (in input sentence)", 'function']]:
#     for i in range (len(function_chunks)):
#         sns.displot(
#             data=df[df['function'].isin(function_chunks[i]) == True].reset_index(drop=True),
#             x="Amount of misspells (in input sentence)", y=col, col="function", hue='function', aspect=.7,)
#         plt.show()


# %%  radar plot libraries and load data
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=df['Damerau–Levenshtein normalized similarity'].values,
      theta=df['function'].values,
      fill='toself',
      name='Product A'
))
fig.add_trace(go.Scatterpolar(
      r=df['Jaro-Winkler normalized similarity'].values,
      theta=df['function'].values,
      fill='toself',
      name='Product A'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 1]
    )),
  showlegend=True
)

fig.show()