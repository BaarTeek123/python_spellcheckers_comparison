import textdistance

from Sentence_comparison.string_metrics import Distance

template_string = 'test'
string_1 = 'a'

print(Distance(string_1, template_string).__dict__)
string_1 = 'test'
print(Distance(string_1, template_string).__dict__)
string_1 = 'test '
print(Distance(string_1, template_string).__dict__)




# for err in rand_df['amount_of_errors'].unique():
#     rand_result = rand_df[rand_df['amount_of_errors'] == err].groupby('function')['damerau_levenshtein_distance'].agg(
#         [('counter', lambda x: (x < 3).sum()), ('total_count', 'count')]).sort_values(by='counter',
#                                                                                       ascending=False).reset_index()
#     rand_result['counter'] = rand_result['counter'] / rand_result['total_count']
#     print(rand_result.sort_values(by='counter', ascending=False).reset_index().head(10))




# f = plt.figure(figsize=(14, 20))
# gs = f.add_gridspec(len(rand_df['amount_of_errors'].unique())+1, 2)
