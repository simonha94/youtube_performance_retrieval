import pandas as pd
from typing import List, Dict
# groupings
def get_work_query_df(df):

    def __get_agg() -> Dict:
        # get the agg
        agg = {}
        for col in ['isVariant', 'isVariant_norm', 'new_result']:
            if col in df.columns:
                agg[col] = ['count', 'sum', 'mean']
        return agg

    def __get_by() -> List:
        # get the by
        return [col for col in __get_columns() if col not in ['isVariant', 'new_result', 'isVariant_norm']]

    def __get_columns() -> List:
        # get the columns
        return [col for col in list(df.columns) if col not in ['result_index', 'yt_id', 'matched_shs_perf', 'score']]

    return multi_to_single_cols(df[__get_columns()].groupby(by=__get_by(), as_index=False, sort=False, dropna=False).agg(__get_agg()))


def get_term_df(df, top_only: bool = True):
    def __get_columns():
        return [col for col in df.columns if col not in ['work', 'query_type']]

    def __get_by():
        return [col for col in __get_columns() if col not in get_agg_columns(__get_columns())]

    df = get_work_query_df(df)
    df.loc[df.keyword == '(none)', 'top_frequency'] = 0

    return df[__get_columns()].groupby(by=__get_by(), as_index=False, dropna=top_only).mean()


def get_agg_columns(columns):
    return [col for col in columns if ('mean' in col or 'sum' in col or 'count' in col or 'rank' in col)]


def get_video_level_columns():
    return ['result_index', 'yt_id', 'matched_shs_perf', 'score', 'isVariant']


def get_indiv_rank_df(df):
    def __get_columns():
        return [col for col in df.columns if col not in ['work', 'query_type', 'keyword', 'top_rank']]

    df = get_work_query_df(df)
    return df[__get_columns()].groupby(by=['with_artist', 'indiv_rank'], as_index=False, dropna=True).mean()


def multi_to_single_cols(df):

    def __col_to_single(col):
        if col[1] in ['mean', 'count', 'sum']:
            return '_'.join(col)
        else:
            return col[0]

    df.columns = [__col_to_single(col) for col in df.columns.values]
    return df


def get_work_query_precision_df(df, new_result=False):
    
    df = get_work_query_df(df)
    df['precision'] = df['isVariant']['sum'] / df['isVariant']['count']
    
    if new_result:
        df['new_results_ratio'] = df['new_result']['sum'] / df['new_result']['count']
        
    return df


def get_yt_results_df():
    try:
    
        df_yt_results = pd.read_csv('csv_data/eval/automatic_eval_videos.csv', sep=';')
    
    except FileNotFoundError:
    
        print("File not found, computing inverse list")
	    # aggregation
        df_yt_results = df.groupby(['work', 'yt_id', 'score', 'isVariant'], as_index=False).agg(list)
	
        #  add new metric column
        df_yt_results['isVariant_norm'] = df_yt_results['isVariant'].astype('int64') / df_yt_results['with_artist'].apply(lambda x: len(x))
       
    return df_yt_results


def attach_norm_isvariant(df):
	
	return pd.merge(df, get_yt_results_df()[['yt_id', 'isVariant_norm']], on='yt_id', how='left')
 
 
def get_query_type_df(df):

    def __get_columns():
        return get_agg_columns(df.columns) + ['with_artist', 'query_type', 'isVariant', 'new_result']
    return pd.concat([df, df[(df.query_type == 'indiv') & (~df.top_rank.isna())].assign(query_type='top')])[__get_columns()].groupby(by=['with_artist', 'query_type'], as_index=False).mean()
