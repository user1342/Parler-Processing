# Parler-Processing
A repository of Python scripts used for the processing of the Parler social network dataset from Aliapoulios et al.

## Process:
### Read the paper and download the dataset
Aliapoulios et al. released a paper called [An Early Look at the Parler Online Social Network](https://arxiv.org/pdf/2101.03820.pdf) containing a first look at the Parler social network. This paper presents a dataset of  98.5M public posts and
84.5M public comments from a random set of 4M users. The [dataset can be found here](https://arxiv.org/pdf/2101.03820.pdf).

### Run the tooling
#### body-aggregation.py
This script is used on a a corpus of Json file Parler posts and users, extracting the body of the post and user information (follow/ following ratio and post frequency). This script creates a single corpus (a CSV file) with one post per row.
#### hashtag-bootstrapping.py
A script to be used on the output of the 'body-aggregator' script. This script iterates through all Parler post bodies looking for a root (or series of root) hashtags. Hashtags in the posts containing this root hashtag are stored until all messages have been processed. The process is then continued with this new list of hashtags. The goal is to create a corpus
The goal is to bootstrap far-right hashtags that will be used to split the dataset into a far-right corpus, and non-far-right corpus.
#### count-hashtags.py
A script for counting the range of hashtags in a data. To be run after the hashtag-bootstrapping.py script on the output of that script and the full corpus.
#### split-dataset.py
A script to be used on the full corpus and a list of far-right hashtags, provided by the output of hashtag-bootstrapping.py. This script will create two sub-corpuses, one which only includes posts containing the far-right hashtags and one of no posts of far-right hashtags.
