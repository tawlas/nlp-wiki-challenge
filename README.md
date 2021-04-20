> The goal of this project is to create clusters of articles of a same topic from a pool of articles. Two methods are used: Graph clustering and Machine learning-based methods.

## **Getting started**

### **Prerequisites**

- Python 3.x (3.7 recommended)

#### _If Python is not installed:_

You can download Python on its official webpage: https://www.python.org/downloads/.

Choose a Python 3 release (Python 3.7 is recommended) that is compatible with your OS.

### **Installing**

We suppose that you have already installed the prerequisites.

#### _Installing requirements_

To do this, open a terminal and go to the project root folder. Then, type:

```
pip install -r requirements.txt
```

### **Project Organization**:

#### _Project template_

Cookiecutter is a CLI tool (Command Line Interface) to create an application boilerplate from a template. It uses a templating system — Jinja2 — to replace or customize folder and file names, as well as file content. We use Cookiecutter to save time constructing a new repository, to avoid forgetting mandatory files like Readme or Changelog; and to lower the entry level to new collaborators — new team members, freelancers, partners. We also use it as a way to enforce standards: you can see it as an invitation to the developer to follow the established rules: make tests and check coverage , write documentation, follow a particular naming syntax… By giving them the structure and the boilerplate code, it makes it easier for developers to do things right.

#### _Project Structure_

    .
    ├── README.md
    ├── README.rst
    ├── config.yml
    ├── data
    │   ├── mi
    │   ├── output
    │   ├── source
    │   │   ├── dataset_business_technology_cybersecurity.pickle
    │   │   └── stopwords.txt
    │   └── test
    │       └── test_data.json
    ├── docs
    ├── main.py
    ├── notebooks
    │   ├── classification.ipynb
    │   └── clustering.ipynb
    ├── requirements.txt
    ├── test.py
    └── wiki_challenge
        ├── Engine.py
        ├── __init__.py
        ├── classes
        │   ├── Extract.py
        │   ├── Graph.py
        │   ├── Load.py
        │   ├── Transformation.py
        │   └── __init__.py
        └── utils
            ├── __init__.py
            ├── clustering.py
            ├── my_workers.py
            ├── preprocessing.py
            └── utils.py

#### _High level organization_

The root folder contains mainly:

- the configuration files required to install the project program.
- a folder named wiki_challenge that contains different python modules organized into subfolders (see project folder).
- main.py, the script to run to launch the End to End Pipeline of part 1.
- test.py, the test script for testing the application (see Unit tests part inside clustering.ipynb)

The code for the different parts of the challenge are organized into different files and folders. Part 1 and Part 2 of the challenges are separated into two jupyter notebooks inside `wiki_challenge` folder located at the root of this project:
Part 1 is achieved inside `clustering.ipynb` and Part 2 inside `classification.ipynb`.
Inside each notebook is a plan outlining the different parts of the notebook.
That being said, the End to End Pipeline command line script of Part 1 is run with `main.py` which is importing different modules located inside `wiki_challenge` folder.

#### _Configuration_

I am using a yaml configuration file named `config.yml` containing all the parameters of our program. Thus, we do not need to specify any extra arguments in the command line interface.

### **Notebooks**

There are two notebooks located under **wiki_challenge** folder: _clustering.ipynb_ and _classification.ipynb_.
_clustering.ipynb_ deals with the first part of the challenge and _classification.ipynb_ the second part.

### **Launching the End to End Pipeline of part 1**

To do so, go to the root project folder in a terminal and type enter the following command:

```
python3 main.py
```

### **Running the tests**

To run the tests, go to the root project folder in a terminal and execute the following command:

```
python3 test.py
```

## **Built with**

- [Python 3](https://www.python.org/)

## **Authors**

- Alassane Watt

## **License**
