import pickle
import yaml


class Extract:
    """Class that loads the input data from the data folder.
    The input data are the wikipedia articles and the stopwords.
    """

    def __init__(self, articles_path, stopwords_path):
        """Stores the passed in data in the class

        :param articles_path: The path to the wikipedia articles.
        :type articles_path: str
        :param stopwords_path: The path to the stopwords.
        :type stopwords_path: str
        """
        self.articles_path = articles_path
        self.stopwords_path = stopwords_path

    def __get_articles_data(self):
        """Loads the wikipedia articles.

        :return: A list of wikipedia articles
        :rtype: list
        """
        with open(self.articles_path, 'rb') as f:
            articles = pickle.load(f)
        return articles

    def __get_stopwords_data(self):
        """Loads an english stopwords list

        :return: A list of english stopwords
        :rtype: list
        """
        with open(self.stopwords_path) as f:
            stopwords = [word.strip() for word in f.readlines()]
        return stopwords

    def get_data(self):
        """Loads and aggregates the wikipedia articles and the stopwords into a dict.

        :return: A dict of data with 2 keys. One for the articles and the other for the stopwords. 
        :rtype: dict
        """
        articles = self.__get_articles_data()
        stopwords = self.__get_stopwords_data()
        data_dict = {'articles': articles, 'stopwords': stopwords}

        return data_dict
