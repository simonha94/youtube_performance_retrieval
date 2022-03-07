# youtube_performance_retrieval
This is the repository containing the data for our submitted paper "Retrieving Music Performances from YouTube: How to formulate effective Search Queries?"

In the main directory, following files are stored:
- `da-tacos.csv`: a metadata overview of all the works including the SHS IDs (work and performance), title, artist, bin ID and language
- `artist_suggestions.csv`: YouTube suggestions of artist+title base query and counts based on the whole dataset 
- `title_suggestions.csv`: YouTube suggestions of title base query and counts based on the whole dataset 
- `csv_data`:
  - `automatic_eval.csv`: one line per YouTube result containing the query information (query type, expansion and the metadata of the work queried for) as well as the aggregated move score of k pairs as explained in the paper 
  - `manual_eval.csv`: one line per YouTube result and original pair with the evaluations by the human raters  
- `json_data`:
  - `query_result_mapping`: contains one JSON per work; filenames are the SHS work IDs. The first level key corresponds to the base query ("title" or "combined"), the second level key to the query type ("", "indiv", "top"=universal) and the third to the expansion (e.g. "live", "cover")
  - `suggestions`: contains one JSON per work which include the YouTube suggestions as received by the API
