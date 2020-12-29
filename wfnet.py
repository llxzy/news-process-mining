import pm4py
import pandas as pd
import os
import sys

from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter


def load_frame(fname: str) -> pd.DataFrame:
    df = pd.read_csv(fname, sep=',')
    return df.sort_values('date')


def process_dataframe(dataframe: pd.DataFrame) -> None:
    """
    First generates the dfg for the entire dataset
    Then calls process_by_type which creates outputs for magazines and newspapers
    and then for each of the publishers separately
    """
    if not os.path.exists("images"):
        os.mkdir("images")
    print("Processing: Entire dataset")
    df_to_image(dataframe, "images/total.png")
    process_by_type(dataframe)
    publishers = set(dataframe['publication'].to_list())
    for publisher in publishers:
        print(f"Processing: {publisher}")
        frame = dataframe[dataframe['publication'] == publisher]
        path = f"images/{publisher}.png"
        df_to_image(frame, path)


def process_by_type(dataframe: pd.DataFrame) -> None:
    """
    Split the source publications into daily newspapers and magazines
    and generated a separate dfg for each
    """
    magazines = ["Gizmodo", "Hyperallergic", "Mashable", "New Republic", "New Yorker",
                 "People", "Refinery 29", "TMZ", "TechCrunch", "The Verge", "Vice", "Wired"]
    magazine_path = f"images/magazines.png"
    news_path = f"images/news.png"
    magazine_frame = dataframe[dataframe['publication'].isin(magazines)]
    news_frame = dataframe[~dataframe['publication'].isin(magazines)]
    print("Processing: magazines")
    df_to_image(magazine_frame, magazine_path)
    print("Processing: newspapers")
    df_to_image(news_frame, news_path)
    

def df_to_image(dataframe: pd.DataFrame, path: str) -> None:
    frame = pm4py.format_dataframe(dataframe, case_id='publication', timestamp_key='date', activity_key='score')
    save_dfg(frame, path)


def save_dfg(dataframe: pd.DataFrame, out_path: str) -> None:
    graph, start_act, end_act = pm4py.discover_dfg(dataframe)
    pm4py.save_vis_dfg(graph, start_act, end_act, out_path)
    

def view_output(dataframe: pd.DataFrame) -> None:
    dfg, start, end = pm4py.discover_dfg(dataframe)
    pm4py.view_dfg(dfg, start, end)


def main():
    process_dataframe(load_frame(sys.argv[1]))
    print("\nDone. Output available at './images'")


if __name__ == "__main__":
    main()
