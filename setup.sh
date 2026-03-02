#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip3 install --quiet --upgrade pip
pip3 install --quiet -e .

pip3 install --quiet \
    docutils \
    furo \
    ipykernel \
    nbsphinx \
    pygments \
    pytest \
    sphinx \
    sphinx_copybutton \
    sphinx_rtd_theme \
    sphinx-autodoc-typehints \
    sphinx-intl \
    sphinx-toggleprompt 

python3 -m spacy download en_core_web_lg
python3 -m nltk.downloader averaged_perceptron_tagger
python3 -m nltk.downloader punkt

pip3 install 'urllib3<2.0' 

# pip3 install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz 

# python3 -m pip install pandas-stubs
# python3 -m pip install types-tqdm
# python3 -m pip install types-colorama
