# Process mining analysis of news articles  

## Overview

A school project with the goal of analysing a dataset of news articles with sentiment analysis, then feeding the resulting opinions into pm4py and creating directly-follow graphs which can be analysed.

The dataset used is ```all-the-news```, available [here](https://components.one/datasets/all-the-news-2-news-articles-dataset/) (all credits go to the team at Components).  

The dataset contains news articles from several news sources. This data is parsed using pandas, fed to a sentiment analyzer and assigned one of three labels: positive, negative and neutral.  
Based on these three labels, the results of analysis are parsed into a dfg using pm4py and saved as images.

### Some notes

- the ```analyze-csv.py``` algorithm is incredibly inefficient, left in an just-works state  
- there is no error checking on arguments to scripts
- related to that, the script obviously works only on the dataset available from the link above, feeding it any other file might require editing the script
- I have never done sentiment analysis before. Thus the one used is vader, as provided by nltk, however it is not the perfect fit and may be replaced later
