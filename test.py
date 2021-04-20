#!/usr/bin/env python
"""Tests module."""
import unittest
import yaml
import os
import json
from collections import Counter


from wiki_challenge.classes.Graph import Graph
from wiki_challenge.utils.clustering import DFS_complete
from wiki_challenge.utils.preprocessing import remove_tags, concatenate_title_and_text, remove_special_chars, tokenize

with open(os.path.abspath(os.path.join(".", "config.yml")), 'r') as ymlfile:
    config = yaml.load(ymlfile, yaml.SafeLoader)

with open(config['paths']['test']) as f:
    test_data = json.load(f)
    for a in test_data:
        a['tokens_count'] = Counter(a['text'])


class Test(unittest.TestCase):

    def test_remove_tags(self):
        """Tests remove_tags function
        """
        html_tags_text = '<p class="mw-empty-elt"></p>Removed the html tags<p><b>Accounting</b>'
        expected_text = "  Removed the html tags  Accounting "
        text = remove_tags(html_tags_text)
        self.assertEqual(text, expected_text)

    def test_concatenate_title_and_text(self):
        """Tests concatenate_title_and_text function
        """
        title = "title"
        content = "content"
        expected_text = "title content"
        text = concatenate_title_and_text(title, content)
        self.assertEqual(text, expected_text)

    def test_remove_special_chars(self):
        """Tests remove_special_chars function
        """
        special_text = "This @ is a 2000$ laptop|%."
        expected_text = "This is a 2000$ laptop"
        text = remove_special_chars(special_text)
        self.assertEqual(text, expected_text)

    def test_tokenize(self):
        """Tests tokenize function
        """
        text = "My name is Alassane"
        expected_tokens = ["My", "name", "is", "Alassane"]
        tokens = tokenize(text)
        self.assertListEqual(tokens, expected_tokens)

    def test_connected_components(self):
        """

        Test data is composed of 9 articles; 3 of each topic.
        The corresponding titles are [Accounting, Finance, Authentication, Multi-factor authentication, Access control, 
        Computer science, Computational science, Theory of computation, Commerce]
        With a connectivity threshold of 15 the coupled titles of connected articles are the following:

        Accounting | Finance
        Access control | Multi-factor authentication
        Authentication | Multi-factor authentication
        Computer science | Theory of computation
        Computer science | Computational science
        Theory of computation | Computational science

        So there are 4 clusters:
        Cluster1:
        Accounting, Finance

        Cluster2:
        Access control, Multi-factor authentication, Authentication,

        Cluster 3:
        Computer science, Theory of computation, Computational science

        Cluster 4:
        Commerce
        """

        true_clusters = ['Accounting/Finance', 'Access control/Authentication/Multi-factor authentication',
                         'Computational science/Computer science/Theory of computation',
                         'Commerce'
                         ]
        connectivity_threshold = 15

        g = Graph(test_data, connectivity_threshold, unique=True)
        _, clusters = DFS_complete(g)

        cluster_titles_all = [set(vertex.element()['title']
                                  for vertex in clusters[key]) for key in clusters.keys()]

        computed_clusters = ["/".join(sorted(cluster))
                             for cluster in cluster_titles_all]
        self.assertEqual(set(true_clusters), set(computed_clusters))


if __name__ == '__main__':
    unittest.main()
