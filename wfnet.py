import pm4py
import pandas as pd
import os
import sys

from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter


def load_frame(fname: str) -> pd.DataFrame:
    df = pd.read_csv(fname, sep=',')
    return df.sort_values('date')


def df_by_publisher(dataframe: pd.DataFrame) -> None:
    publishers = set(dataframe['publication'].to_list())
    if not os.path.exists("images"):
        os.mkdir("images")
    for publisher in publishers:
        print(f"Processing: {publisher}")
        frame = dataframe[dataframe['publication'] == publisher]
        frame = pm4py.format_dataframe(frame, case_id='publication', timestamp_key='date', activity_key='score')
        path = f"images/{publisher}.png"
        save_dfg(frame, path)


def df_entire(dataframe: pd.DataFrame) -> None:
    print("Processing: Entire dataset")
    frame = pm4py.format_dataframe(dataframe, case_id='publication', timestamp_key='date', activity_key='score')
    if not os.path.exists("images"):
        os.mkdir("images")
    path = f"images/total.png"
    save_dfg(frame, path)


def save_dfg(dataframe: pd.DataFrame, out_path: str) -> None:
    graph, start_act, end_act = pm4py.discover_dfg(dataframe)
    pm4py.save_vis_dfg(graph, start_act, end_act, out_path)
    

def view_output(dataframe: pd.DataFrame) -> None:
    dfg, start, end = pm4py.discover_dfg(dataframe)
    pm4py.view_dfg(dfg, start, end)


def main():
    dataframe = load_frame(sys.argv[1])
    
    df_by_publisher(dataframe)
    df_entire(dataframe)
    print("\nDone. Output available at './images'")


if __name__ == "__main__":
    main()
