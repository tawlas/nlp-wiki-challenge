"""This file contains preprocessing related helper functions.
"""

import re
from collections import Counter


# ** exploratory data analysis
# Removes duplicate articles
def remove_duplicate_articles(articles, verbose=False):
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


# Identifying each article
def get_title_to_id_dict(titles):
    """Creates a dict mapping each title with an id.

    :param titles: list of titles
    :type titles: list
    :return: dict mapping a title to an id.
    :rtype: dict
    """
    title_to_id = {title: i for i, title in enumerate(titles)}
    return title_to_id


# ** Data preprocessing part

# Gets the summary of a wikipedia article
def get_summary(html_text):
    """Returns the summary part of the raw html text string of the wikipedia article.

    :param html_text: The html content of an article.
    :type html_text: str
    :return: The summary of the input wikipedia article.
    :rtype: str
    """
    # The summary ends before the first h tag.
    end_summary_index = html_text.find('<h')
    summary = html_text[:end_summary_index]
    return summary


# remove tags
def remove_tags(html_text):
    """Removes the html tags in a wikipedia article.

    :param html_text: the html text of a wikipedia article.
    :type html_text: str
    :return: Tag removed wikipedia article.
    :rtype: str
    """
    tags_regex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    tag_free_text = re.sub(tags_regex, ' ', html_text)
    return tag_free_text


# combine title and content of article
def concatenate_title_and_text(title, text):
    """Concatenates title and content of an article in the same string.
    The two parts are separated by a blank space.

    :param title: The tile of an article
    :type title: str
    :param text: The text content of an article
    :type text: str
    :return: The string resulting from the blank space based concatenation of the input data.
    :rtype: str
    """
    content = " ".join([title, text])
    return content


# remove special chars
def remove_special_chars(raw_text):
    """Removes the special characters in a given article based on some regex.

    :param raw_text: full text with special characters
    :type raw_text: str
    :return: Special character free article
    :rtype: str
    """
    spec_free_text = re.sub(r'[^A-Za-z0-9\$]+', ' ', raw_text).strip()
    return spec_free_text


# add token counts
def add_tokens_count(article):
    """Add a count dict of the tokens of an article as a new key to the article dict.

    :param article: an article dict
    :type article: dict
    :return: input dict with a new key-value pair whose value being a python Counter of the tokens.
    :rtype: dict
    """
    article['tokens_count'] = Counter(article['text'])
    return article


# tokenization
def tokenize(content):
    """Computes a python Counter on the tokens of an article and adds it as a key-value pair in the article dict.

    :param article: An article dict
    :type article: dict
    :return: the updated article dict with a python Counter of the article tokens.
    :rtype: dict
    """
    return content.split(" ")


# remove stopwords
def remove_stop_words(content, stopwords):
    """Removes the stopwords in an article.

    :param tokens: The tokens of an article.
    :type tokens: []str
    :param stopwords: the list of stopwords
    :type stopwords: []str
    :return: The tokens of an article that are not stopwords.
    :rtype: []str
    """
    return [token for token in content if token not in stopwords]


# apply above preprocessing steps on a single article
def preprocess_article(article, stopwords, summary, title):
    """Applies all the processing steps on the input article

    :param articles: The wikipedia articles
    :type articles: list
    :param stopwords: list of stop-words
    :type stopwords: list
    :param summary: when True, only keeps the summary content, defaults to False
    :type summary: bool, optional
    :param title: Whether to include the title as a feature, defaults to True
    :type title: bool, optional
    :return: preprocessed article
    :rtype: dict
    """
    text = article['content']
    title = article['title']

    if summary:
        # get the summary of the wikipedia article
        text = get_summary(text)
    # remove tags
    text = remove_tags(text)
    if title:
        # concatenate
        text = concatenate_title_and_text(title, text)
    # lower case
    text = text.lower()
    # remove special chars
    text = remove_special_chars(text)
    # tokenization
    text = tokenize(text)
    # remove stopwords
    text = remove_stop_words(text, stopwords)

    article['text'] = text
    # add words count
    article = add_tokens_count(article)
    return article


# apply above preprocessing steps on a all articles
def preprocess_articles(articles, stopwords, summary=False, title=True):
    """Applies all the processing steps on the given article dataset

    :param articles: The wikipedia articles
    :type articles: list
    :param stopwords: list of stop-words
    :type stopwords: list
    :param summary: when True, only keeps the summary content, defaults to False
    :type summary: bool, optional
    :param title: Whether to include the title as a feature, defaults to True
    :type title: bool, optional
    :return: list of preprocessed articles
    :rtype: list
    """

    articles = list(
        map(lambda article: preprocess_article(article, stopwords, summary, title), articles))

    print(f'Preprocessing of {len(articles)} artilces succesfully done!')
    return articles
