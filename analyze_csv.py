from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import pandas as pd
import csv
import os

"""
some of the articles were longer than the default field size
"""
csv.field_size_limit(2**20)


def process_row(
    row     : pd.Series, 
    analyzer: SentimentIntensityAnalyzer, 
    ds      : list, 
    ts      : list, 
    ps      : list, 
    sc      : list
    ) -> None:

    """
    'Chevron in article' removes annoying articles containing remaining site data
    not enough of them to bother parsing them out separately, but enough to distort results if included
    """
    article = row['article']
    if type(article) != str or "Chevron" in article:
        return
    n = p = 0
    for sentence in tokenize.sent_tokenize(article):
        scores = analyzer.polarity_scores(sentence)
        n += scores['neg']
        p += scores['pos']

    if n > p:
        article_score = "negative"
    elif p > n:
        article_score = "positive"
    else:
        article_score = "neutral"

    ts.append(row['title'])
    ds.append(row['date'])
    ps.append(row['publication'])
    sc.append(article_score)


def process_dataframe(df: pd.DataFrame, analyzer: SentimentIntensityAnalyzer, output_fname: str) -> None:
    dates, titles, publications, article_scores = [], [], [], []

    for _, row in df.iterrows():
        process_row(row, analyzer, dates, titles, publications, article_scores)

    data = {
        "title"       : titles,
        "date"        : dates,
        "publication" : publications,
        "score"       : article_scores
    }

    df = pd.DataFrame(data)
    df.to_csv(output_fname, mode='a', header=not(os.path.exists(output_fname)))


def get_data_allnews(fname: str, default_chunk_size: int=2048) -> str:
    chunk_index = 0
    sent_analyzer = SentimentIntensityAnalyzer()
    output_fname = fname.split(".csv")[0] + "-output.csv"
    for chunk in pd.read_csv(
                    fname, 
                    sep=',',
                    encoding='utf-8',
                    usecols=['date', 'title', 'article', 'publication'],
                    chunksize=default_chunk_size, 
                    engine="python",
                    error_bad_lines=False
                    ):
        print(f"Processing chunk [{chunk_index}]")
        chunk_index += 1
        process_dataframe(chunk, sent_analyzer, output_fname)
    return output_fname
    

def main(fname: str):
    print(f"Processing data at '{fname}'")
    out_file = get_data_allnews(fname)
    print(f"Created output at '{out_file}'")


if __name__ == "__main__":
    main("all-the-news-900k.csv")
