# Backend coding challenge

## Task

Using the New York Times API (specifically Article Search) return news items in
a Python dictionary format.

See developer.nytimes.com for the API documentation of the New York
Times.

## Setup

Tools needed:
Only Python 3

## Executing the File

1. Make sure to have python installed on the machine.
2. On terminal or command prompt, navigate to the directory where backend-coding-challenge.py file is located.
3. Run the script using the following command:

```
python backend-coding-challenge.py
```

Additionally, I provided some arguments option to be parsed on command line. All of these arguments are optional and they are provided in order to give more flexibility when retrieving the articles from the NY times api. Here is a brief description of each argument:

Example

```
python backend-coding-challenge.py --query 'Meta Threads' --begin_date 2023-01-01 --end_date 2023-07-07
```

1. --query : Optionally Specify the search query for the articles. This is used to modify the search for articles related to different topic. The default value is 'Silicon Valley'.
2. --begin_date : Optionally specify the begin date for the articles in the format "YYYYMMDD". This filters the articles to be retrieved based on their publication date. Omit this argument if you want to retrieve articles without any specific date range. The default value is 2023-01-01
3. --end_date : Optionally specify the end date for the articles in the format "YYYYMMDD". This further narrows down the date range for the articles to be retrieved. Omit this argument if you want to retrieve articles without any specific end date.

Note: The articles retrieved are sorted by the latest published date.
