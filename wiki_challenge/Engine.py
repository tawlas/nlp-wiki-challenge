import yaml
import os

from .classes.Extract import Extract
from .classes.Transformation import Transformation
from .classes.Load import Load


# Loading the configuration file
with open(os.path.abspath(os.path.join(".", "config.yml")), 'r') as ymlfile:
    config = yaml.load(ymlfile, yaml.SafeLoader)


class Engine:
    """Class executing the entire pipeline of clustering.
    """

    def __init__(self):
        pass

    def __extract_data(self):
        """Loads in the data used in the project.

        :return: A dict of data as returned by the get_data method of the Extract class.
        :rtype: dict
        """
        articles_path = os.path.abspath(
            config['paths']['data_sources']['articles'])
        stopwords_path = os.path.abspath(
            config['paths']['data_sources']['stopwords'])

        extract = Extract(articles_path, stopwords_path)
        data = extract.get_data()
        return data

    def __transform_data(self, data):
        """Preprocesses the data, then computes the clusters, and finally analyzes the data.

        :param data: A dict with 2 keys. One mapping to the articles dataset and the other to the stopwords list.
        :type data: dict
        :return: clusters dict. (See internal methods docstrings for more details.)
        :rtype: dict
        """
        connectivity_threshlod = int(
            config['parameters']['connectivity_threshold'])
        transform = Transformation(data, connectivity_threshlod)
        clusters = transform.get_articles_clusters()
        return clusters

    def __load(self, clusters):
        """Saves the result clusters to disk.

        :param clusters: clusters dict
        :type clusters: dict
        """
        output_path = config['paths']['output']['clusters']
        load = Load(output_path)
        load.save(clusters)

    def run(self):
        """Runs the Extract Transform Load pipeline of this project.
        """
        print("************* Start! *****************")
        print("************* Extracting data... *****************")
        data = self.__extract_data()
        print("************* Data extracted *****************")
        print("************* Transforming data... *****************")
        clusters = self.__transform_data(data)
        print("************* Transformation is done *****************")
        print("************* Saving data *****************")
        self.__load(clusters)
        print("************* End! *****************")
