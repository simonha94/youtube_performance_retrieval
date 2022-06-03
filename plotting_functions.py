from helper_functions import grouping_functions
# plotting functions
import seaborn as sns
import matplotlib.pyplot as plt

def plot_topk_mean_precision(df, top_k, filename='topk_precision.pdf'):

	def __get_rank(term):
		if term == '(none)':
			return '0'
		return str(list(top_k[0]).index(term) + 1)

	data = grouping_functions.get_work_query_precision_df(df, True)[['with_artist', 'keyword', 'top_rank', 'precision', 'new_results_ratio']].groupby(by=['with_artist', 'keyword', 'top_rank'], as_index=False).mean()
	data = data.sort_values(by='precision', ascending=False)

	data['rank'] = data.apply(lambda x: __get_rank(x['keyword'].item()), axis=1)
	data['keyword'] = data.apply(lambda x: __get_rank(x['keyword'].item()) + ' ' + x['keyword'].item(), axis=1)

	plot_barchart(data, 'keyword', "precision", 'Expansion Term', 'Mean Precision', "Base Query", True, filename)


def plot_terms_topk_mean_precision(df, top_k, filename='topk_precision.pdf'):
	def __get_rank(term):
		if term == '(none)':
			return '0'
		return str(list(top_k[0]).index(term) + 1)

	df = grouping_functions.get_term_df(df)
	df['rank'] = df.apply(lambda x: __get_rank(x['keyword']), axis=1)
	df['keyword'] = df.apply(lambda x: __get_rank(x['keyword']) + ' ' + x['keyword'], axis=1)

	multi_barplots(df, 'keyword', 'Expansion Term', filename)


def plot_terms_indiv_rank_precision(df, filename='indiv_terms_precision.pdf'):
	
	df = grouping_functions.get_indiv_rank_df(df)
	multi_barplots(df, 'indiv_rank', 'Indiv. Expansion Rank', filename)

	
def plot_query_type_mean_precision(df, filename='query_type_precision.pdf'):

	plot_barchart(grouping_functions.get_query_type_df(df), "query_type", "isVariant", "Query Type","Mean Precision", "Base Query", True, filename)


def multi_barplots(df, x, xlabel, filename):

	fig, axes = plt.subplots(3, 1, figsize=(10, 15))
	#fig.suptitle('Initial Pokemon - 1st Generation')
	for i, prec_col in enumerate([col for col in df.columns if 'mean' in col]):

		df = df.sort_values(by=prec_col, ascending=False)
		sns.barplot(ax=axes[i], data=df, x=x, y=prec_col, hue='with_artist')
		# labels
		axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45, horizontalalignment='right')
		axes[i].set(xlabel=xlabel, ylabel='Mean Precision')
		axes[i].legend().set_title('Base Query')

		fig.tight_layout()
		axes[i].set_title(prec_col.replace('_mean', ''))
	fig.savefig(f'plots/{filename}')

def plot_barchart(data, x, y, xlabel, ylabel, legendtitle, rotate: bool, filename):

	ax = sns.barplot(data=data, x=x, y=y, hue="with_artist", ci="sd", palette="dark", alpha=.6)

	#labels
	if rotate:
		ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
	ax.set(xlabel=xlabel, ylabel=ylabel)

	ax.legend().set_title(legendtitle)

	plt.tight_layout()
	plt.savefig(f'plots/{filename}')