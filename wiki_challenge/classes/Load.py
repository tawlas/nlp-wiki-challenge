import pickle
import os
import datetime


class Load:
    """Class taking care of saving the computed clusters in disk.
    """

    def __init__(self, output_path):
        """Stores the output path to save the clusters in.

        :param output_path: Path where to save the computed clusters.
        :type output_path: str
        """
        self._output_path = output_path

    def save(self, clusters):
        """Saves the clusters to disk with a timestamp in pickle format

        :param clusters: dict of clusters
        :type clusters: dict
        """
        doc_name, doc_extension = tuple(self._output_path.split('.'))
        time_stamp = "{}".format(datetime.datetime.now().strftime("%H:%M:%S"))
        output_path = os.path.abspath(
            doc_name + '_' + time_stamp + '.' + doc_extension)
        with open(output_path, 'wb') as f:
            pickle.dump(clusters, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Clustering results are saved at: {}".format(output_path))
