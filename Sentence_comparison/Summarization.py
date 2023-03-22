import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def three_sigma(data_frame: pd.DataFrame):
    return data_frame.loc[(data_frame[data_frame.columns[0]] < (
        round(data_frame[data_frame.columns[0]].mean() + 3 * round(df[data_frame.columns[0]].std())))) & (
                                  data_frame[data_frame.columns[0]] > (round(
                              data_frame[data_frame.columns[0]].mean() - 3 * round(df[data_frame.columns[0]].std()))))]


def data_frame_summary(data_frame: pd.DataFrame) -> pd.DataFrame:
    data = {}
    ids = ['median', 'variance', 'skew']
    for col_name in data_frame.columns:
        data[col_name] = []
        data[col_name].append(round(data_frame[col_name].median(), 2))
        data[col_name].append(round(data_frame[col_name].var(), 2))
        data[col_name].append(round(data_frame[col_name].skew(), 2))
    return pd.concat([data_frame.describe(), pd.DataFrame(data=data, index=ids)])


def get_dictionary_distribution(data_dictionary: dict) -> dict:
    for k in data_dictionary.keys():
        data_dictionary[k] = int(len(data_dictionary[k]))
    return data_dictionary



if __name__ == "__main__":
    directory = 'C:\\Users\\user\\PycharmProjects\\tool_comparer\\results'
    file_path = '../Archive/second.xlsx'
    worksheet_names = pd.read_excel(file_path, None).keys()

    i = 1
    lev, d_lev = pd.DataFrame(), pd.DataFrame()
    df = None

    for sheet in worksheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, usecols='C:G')
        if 'spell' not in sheet[:6]:
            df = three_sigma(df)
        data = data_frame_summary(df)
        with pd.ExcelWriter('C:\\Users\\user\\PycharmProjects\\tool_comparer\\first_result.xlsx', mode='a') as writer:
            data.to_excel(writer, sheet_name=sheet, index=True)
        dam_lev_distr = get_dictionary_distribution(df.groupby(['damerau_levenshtein_distance']).groups)
        d_lev = pd.concat([d_lev, pd.DataFrame(dam_lev_distr, index=[sheet])])
        lev_distr = get_dictionary_distribution(df.groupby(['levenshtein_distance']).groups)
        pd.DataFrame(lev_distr, index=[sheet])
        lev = pd.concat([lev, pd.DataFrame(lev_distr, index=[sheet])])
        print(i)
        i += 1
    print(d_lev)
    print(lev)

    file_path = '../Archive/second.xlsx'
    worksheet_names = pd.read_excel(file_path, None).keys()
    # damerau
    for sheet in worksheet_names:
        print(sheet)
        df = pd.read_excel(file_path, sheet_name=sheet, usecols='C:G')
        df = three_sigma(df)
        data = data_frame_summary(df)
        with pd.ExcelWriter('C:\\Users\\user\\PycharmProjects\\tool_comparer\\sec_result.xlsx', mode='a') as writer:
            data.to_excel(writer, sheet_name=sheet, index=True)
        dam_lev_distr = get_dictionary_distribution(df.groupby(['damerau_levenshtein_distance']).groups)
        d_lev = pd.concat([d_lev, pd.DataFrame(dam_lev_distr, index=[sheet])])
        lev_distr = get_dictionary_distribution(df.groupby(['levenshtein_distance']).groups)
        lev = pd.concat([lev, pd.DataFrame(lev_distr, index=[sheet])])
        print(i)
        i += 1

    print(d_lev)
    print(lev)

# write to excel lev and damerau-lev distribution
# with pandas.ExcelWriter('C:\\Users\\user\\PycharmProjects\\tool_comparer\\lev_dam.xlsx', mode='a') as writer:
#         lev.to_excel(writer, sheet_name='Lev', index=True)
#         d_lev.to_excel(writer, sheet_name='Damerau_Lev', index=True)


#     with pandas.ExcelWriter('C:\\Users\\user\\PycharmProjects\\tool_comparer\\result.xlsx', mode='a+') as writer:
#                  df.to_excel(writer, sheet_name=sheet + ' ', index=False)
