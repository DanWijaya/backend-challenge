import argparse
import logging
import requests

log = logging.getLogger(__name__)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """

    def __init__(self):
        self.config = {}

    def connect(self, inc_column=None, max_inc_value=None):
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source in batches.

        :returns One list for each batch. Each of those is a list of
                 dictionaries with the defined rows.
        """
        params = {
            "api-key": "CMLwG3ogAnhyeBFAAEoc3t2aA9o4jcOI",
            "q": self.config.get("query"),
            "sort": "newest",
            "fl": "web_url,headline,snippet,lead_paragraph,source,pub_date",
            "begin_date": self.config.get("begin_date"),
            "end_date": self.config.get("end_date"),
            "page_size": batch_size,
            "page": 0
        }

        page = 0
        while (True):
            params["page"] = page
            articles = self.retrieve_articles(params)
            if not articles:
                break
            yield articles
            page += 1

    def getSchema(self):
        """
        Return the schema of the dataset.
        :returns A list containing the names of the columns retrieved from the source.
        """
        schema = [
            "web_url",
            "headline.main",
            "headline.kicker",
            "snippet",
            "lead_paragraph",
            "source",
            "pub_date"
        ]

        return schema

    @staticmethod
    def flatten_dictionary(dictionary, parent_key="", sep="."):
        """
        :param dictionary: The nested dictionary to be flattened.
        :param parent_key: The parent key of the current dictionary.
        :param sep: The separator to be used for the flattened keys.
        :return: A flattened dictionary.
        """
        items = []
        for key, value in dictionary.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(NYTimesSource.flatten_dictionary(
                    value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)

    @staticmethod
    def retrieve_articles(params):
        base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        response = requests.get(base_url, params=params)
        response_json = response.json()
        articles = []

        if response.status_code == 200:
            response_docs = response_json.get("response", {}).get("docs", [])

            for doc in response_docs:
                flattened_article = NYTimesSource.flatten_dictionary(doc)
                articles.append(flattened_article)

        return articles


def main():

    parser = argparse.ArgumentParser(
        description="Retrieve news articles from the New York Times API")
    parser.add_argument("--query", type=str, default="Silicon Valley",
                        help="Search query (default: 'Silicon Valley')")
    parser.add_argument("--begin_date", type=str,
                        help="(Optional) Begin date for the articles", default="2023-01-01")
    parser.add_argument("--end_date", type=str,
                        help="(Optional) End date for the articles")
    # parser.add_argument("--start_page", type=int,
    #                     help="(Optional) default start page is 0", default=0)
    # parser.add_argument("--end_page", type=int,
    #                     help="(Optional) default end page is 5", default=4)

    args = parser.parse_args()

    config = {
        "query": args.query,
        "begin_date": args.begin_date,
        "end_date": args.end_date,
        # "start_page": args.start_page,
        # "end_page": args.end_page
    }
    source = NYTimesSource()

    # This looks like an argparse dependency - but the Namespace class is just
    # a simple way to create an object holding attributes.
    # source.args = argparse.Namespace(**config)

    source.config = config
    for idx, batch in enumerate(source.getDataBatch(10)):
        print(f"Batch {idx} of {len(batch)} items")
        for item in batch:
            print(f"  - {item['web_url']} - {item['headline.main']}")
            print(item)


if __name__ == "__main__":
    main()
