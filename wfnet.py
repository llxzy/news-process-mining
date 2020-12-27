import pm4py
import pandas as pd
import os
import sys

from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter


def load_frame(fname: str) -> pd.DataFrame:
    df = pd.read_csv(fname, sep=',')
    return df.sort_values('date')


def process_dataframe(dataframe: pd.DataFrame, partial: bool = True) -> None:
    if not os.path.exists("images"):
        os.mkdir("images")
    print("Processing: Entire dataset")
    df_to_image(dataframe, "images/total.png")
    if not partial:
        return
    publishers = set(dataframe['publication'].to_list())
    for publisher in publishers:
        print(f"Processing: {publisher}")
        frame = dataframe[dataframe['publication'] == publisher]
        path = f"images/{publisher}.png"
        df_to_image(frame, path)


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
