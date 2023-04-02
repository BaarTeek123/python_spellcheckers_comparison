import matplotlib.ticker as ticker
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib


def config_plot_for_latex():
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })


def get_plot(df, plot, col_name, x_name: str = None, y_name: str = None, ax_step: int = None):
    ax = plot
    if x_name is not None:
        ax.set_xlabel(f"{x_name}")
    if y_name is not None:
        ax.set_ylabel(f"{y_name}")
    if ax_step is not None:
        plt.xticks(np.arange(np.floor(df[col_name].min()),
                             np.ceil(df[col_name].max()) + 1, ax_step))
    return ax


def get_hist_board(df: pd.DataFrame, function_chunks: list[list], column_name: str, by: str, bins: int = None,
                   title: str = None, file_path: str = None):
    f = plt.figure(figsize=(14, 20))
    gs = f.add_gridspec(7, 2)
    if df[column_name].max() < 1.5:
        binwidth = 0.1
        x_step = 0.1
        xtick_range = 1.0

    else:
        binwidth = 1
        x_step = 1
        xtick_range = df[column_name].max() + x_step

    if bins is None:
        bins = 10

    for i in range(len(function_chunks)):
        # split data to sub chunks
        upper = df[df[by].isin(function_chunks[i][:4]) == True].reset_index(drop=True)
        lower = df[df[by].isin(function_chunks[i][4:]) == True].reset_index(drop=True)

        with sns.axes_style("white"):
            ax = f.add_subplot(gs[i, 0])
            plot = sns.histplot(
                upper,
                bins=bins,
                x=column_name, hue=by,
                palette="pastel",
                edgecolor=".5",
                linewidth=.5,
                multiple='dodge',
                stat="density", common_norm=False, binwidth=binwidth
            )
            get_plot(df, plot, column_name, ax_step=1)
            ax.xaxis.set_ticks(np.arange(0, xtick_range, x_step))
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

        with sns.axes_style("white"):
            ax = f.add_subplot(gs[i, 1])
            plot = sns.histplot(
                lower,
                bins=bins,
                x=column_name, hue=by,
                palette="pastel",
                edgecolor=".5",
                linewidth=.5,
                multiple='dodge',
                stat="density", common_norm=False, binwidth=binwidth
            )
            get_plot(lower, plot, column_name, ax_step=1)
            ax.xaxis.set_ticks(np.arange(0, xtick_range, x_step))
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

    if title is not None:
        f.suptitle(f'{title}')
    ax.legend(fontsize=10)
    f.tight_layout(rect=[0, 0.03, 1, 0.95])
    if file_path is not None:
        plt.savefig(file_path)
    plt.show()



