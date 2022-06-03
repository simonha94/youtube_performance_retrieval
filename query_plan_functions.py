   
# query plan
from tqdm import tqdm

def rank_queries(df):
    return df.sort_values(by=['work', 'query_type', 'query_rank', 'with_artist', 'result_index'])
    
def append_new_result(df):
    
    cur_work = None
    found_yt_ids = []
    new_result = []
    
    for i, row in tqdm(df.iterrows()):
        
        if row.work == cur_work:
            
            new_result.append(row.yt_id not in found_yt_ids) 
            found_yt_ids.append(row.yt_id)
            
        else:
            
            new_result.append(row.yt_id not in found_yt_ids)
            
            cur_work = row.work
            found_yt_ids = []
            
    df['new_result'] = new_result
    return df
            

def simulate_query_plan(df):
    return append_new_result(rank_queries(df))
