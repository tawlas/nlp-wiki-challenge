import pickle
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import re
import copy
import statistics as ss
from .Graph import Graph
# *********************** Preprocessing subclass *********************************


class Preprocessing:
    """Preprocesses the wikipedia articles dataset to return the essential tokens
     of an article in a dict for each one of the articles. A counter is also added to count
     the token distribution for the articles.
    """

    def __init__(self):
        pass

    # Remove duplicates
    def __remove_duplicate_articles(self, articles, verbose=False):
        """Removes duplicate articles in the dataset.

        :param articles: The dataset of wikipedia articles
        :type articles: list
        :param verbose: Boolean indicating whether or not to print info about dataset length, defaults to False
        :type verbose: bool, optional
        :return: Duplicate free articles dataset.
        :rtype: list
        """
        titles = set()
        dup_free_articles = []
        for article in articles:
            title = article['title']
            if title not in titles:
                titles.add(title)
                dup_free_articles.append(article)

        if verbose:
            print('Found and removed {} duplicate articles.'.format(
                len(articles) - len(dup_free_articles)))
            print('New dataset size: {}.'.format(len(dup_free_articles)))

        return dup_free_articles

    def __remove_tags(self, html_text):
        """Removes the html tags in a wikipedia article.

        :param html_text: the html text of a wikipedia article.
        :type html_text: str
        :return: Tag removed wikipedia article.
        :rtype: str
        """
        tags_regex = re.compile(
            '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        tag_free_text = re.sub(tags_regex, ' ', html_text)

        return tag_free_text

    def __remove_special_chars(self, raw_text):
        """Removes the special characters in a given article based on some regex.

        :param raw_text: full text with special characters
        :type raw_text: str
        :return: Special character free article 
        :rtype: str
        """
        spec_free_text = re.sub(r'[^A-Za-z0-9\$]+', ' ', raw_text).strip()

        return spec_free_text

    def __add_tokens_count(self, article):
        """Computes a python Counter on the tokens of an article and adds it as a key-value pair in the article dict.

        :param article: An article dict
        :type article: dict
        :return: the updated article dict with a python Counter of the article tokens.
        :rtype: dict
        """
        article['tokens_count'] = Counter(article['content'])

        return article

    def __tokenize(self, content):
        """Tokenizes an article text into a list of token string with one blank space as a 
        token separator.

        :param content: The text content of an article.
        :type content: str
        :return: A list of tokens
        :rtype: list
        """
        return content.split(" ")

    def __remove_stop_words(self, tokens, stopwords):
        """Removes the stopwords in an article.

        :param tokens: The tokens of an article.
        :type tokens: []str
        :param stopwords: the list of stopwords
        :type stopwords: []str
        :return: The tokens of an article that are not stopwords.
        :rtype: []str
        """
        return [token for token in tokens if token not in stopwords]

    def preprocess_articles(self, articles, stopwords):
        """Applies the preprocessing steps on the articles dataset

        :param articles: the articles dataset.
        :type articles: []dict
        :param stopwords: A list of english stopwords.
        :type stopwords: []str
        :return: The preprocessed articles dataset
        :rtype: []dict
        """
        for article in articles:
            # we copy content to save the original content of the article
            content = copy.deepcopy(article['content'])

            # preprocessing
            # lower case
            content = content.lower()
            # remove tags
            content = self.__remove_tags(content)
            # remove special chars
            content = self.__remove_special_chars(content)
            # tokenization
            tokens = self.__tokenize(content)
            # remove stopwords
            tokens = self.__remove_stop_words(tokens, stopwords)

            # add preprocessed data to the article
            # add tokens
            article['tokens'] = tokens
            # add tokens count
            article = self.__add_tokens_count(article)

        return articles


# *********************** Clustering subclass *********************************

class Clustering:
    """Class aplying a graph-based clustering of the wikipedia articles.
    """

    def __init__(self, connectivity_threshold):
        """Stores the connectivity threshold above which two article nodes are considered connected.

        :param connectivity_threshold: The connectivity threshold above which two article nodes are considered connected.
        :type connectivity_threshold: int
        """
        self._connectivity_threshold = connectivity_threshold

    def __DFS(self, g, u, discovered, cluster):
        """Perform DFS of the undiscovered portion of Graph g starting at Vertex u.

        discovered is a dictionary mapping each vertex to the edge that was used to
        discover it during the DFS. (u should be ”discovered” prior to the call.)
        Newly discovered vertices will be added to the dictionary as a result.

        :param g: a Graph class object
        :type g: Graph
        :param u: a Vertex object from which to discover adjacent nodes.
        :type u: Graph.Vertex
        :param discovered: a dict of discovered nodes. A key in that dict is a
        discovered node and the corresponding value is the tree edge that discovered v
        :type discovered: dict
        :param cluster: A list of nodes belonging in the same cluster.
        :type cluster: list
        """
        for e in g.incident_edges(u):  # for every outgoing edge from u
            v = e.opposite(u)
            if v not in discovered:  # v is an unvisited vertex
                discovered[v] = e  # e is the tree edge that discovered v
                cluster.append(v)
                # recursively explore from v
                self.__DFS(g, v, discovered, cluster)

    def __DFS_complete(self, g):
        """Perform DFS for entire graph and return forest as a dictionary.

        Result maps each vertex v to the edge that was used to discover it.
        (Vertices that are roots of a DFS tree are mapped to None.)

        :param g: a Graph class object
        :type g: Graph
        :return: A tuple of dicts summarizing the clusters of the input graph. The second returned value, 
        that which is of interest in this project, is a dict where a key is a discovery vertex of a cluster
        and its corresponding value is the list of vertices in its cluster.
        :rtype: tuple
        """
        forest = {}
        clusters = {}
        for u in g.vertices():
            if u not in forest:
                forest[u] = None  # u will be the root of a tree
                cluster = [u]
                self.__DFS(g, u, forest, cluster)
                clusters[u] = cluster
        return forest, clusters

    def get_clusters(self, articles):
        """Instanciates a graph object and computes the clusters of that graph object.

        :param articles: A list of articles. Each item is a dict
        :type articles: list
        :return: a cluster dictionnary
        :rtype: dict
        """
        clusters_dict = {}
        g = Graph(articles, self._connectivity_threshold, unique=True)
        forests, clusters = self.__DFS_complete(g)
        clusters_dict['clusters'] = clusters
        clusters_dict['forests'] = forests
        return clusters_dict


# *********************** Analysis subclass *********************************

class Analysis:
    """Class for statistical analysis of the clusters of wikipedia articles.
    """

    def __init__(self):
        """
        """
        pass

    def __compute_clusters_statistics(self, clusters):
        """Computes global statistics about the clusters of articles.

        :param clusters: dict of clusters
        :type clusters: dict
        :return: statistics dict.
        :rtype: dict
        """

        stats = {}
        cluster_sizes = [len(clusters[c]) for c in clusters]
        stats['n_clusters'] = len(clusters)
        stats['mean'] = ss.mean(cluster_sizes)
        stats['stdev'] = ss.stdev(cluster_sizes)
        stats['median'] = ss.median_high(cluster_sizes)
        stats['min'] = min(cluster_sizes)
        stats['max'] = max(cluster_sizes)

        return stats

    def add_clusters_statistics(self, clusters):
        """Computes statistics about the clusters and add them to the clusters dict

        :param clusters: clusters dict
        :type clusters: dict
        :return: clusters dict with additional key called statistics.
        :rtype: dict
        """
        clusters['statistics'] = self.__compute_clusters_statistics(clusters)
        return clusters


# *********************** Transformation class *********************************

class Transformation:
    """Class in charge of applying transformation of the data. 
    """

    def __init__(self, data, connectivity_threshold):
        """Stores passed in args and instantiates Preprocessing, Clustering and Analysis classes.

        :param data: A dict with 2 keys; One being the articles and the other the stopwords.
        :type data: dict
        :param connectivity_threshold: The connectivity threshold above which two article nodes are considered connected.
        :type connectivity_threshold: int | str
        """
        self._articles = data['articles']
        self._stopwords = data['stopwords']
        self._preprocessing_obj = Preprocessing()
        self._clustering_obj = Clustering(connectivity_threshold)
        self._analysis_obj = Analysis()

    def get_articles_clusters(self):
        """Applies the pipeline allowing to compute article clusters.

        :return: A python dict of clusters.
        :rtype: dict
        """
        print("Preprocessing the articles...")
        self._preprocessing_obj.preprocess_articles(
            self._articles, self._stopwords)
        print("Preprocessing is done")
        print("Clustering the articles...")
        clusters = self._clustering_obj.get_clusters(self._articles)
        print("Clustering is done")
        print("Adding clustering statistics...")
        clusters = self._analysis_obj.add_clusters_statistics(clusters)
        print("Added clustering statistics")

        return clusters
