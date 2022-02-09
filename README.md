# Rasa converter 💬

Rasa converter converts Rasa training data [format](https://rasa.com/docs/rasa/next/training-data-format) to a more conventient format
for training outside Rasa. By default this format is a JSONL with that follows the structure below
```
{
    "text": ...,
    "intent": ...,
    "entities": [
        {
            "start_char": ...,
            "end_char": ...,
            "label": ...,
            "text": ...,
        },
        ...
    ]
}
```

# 🛠 Install

```
python -m venv venv
source venv/bin/activate

git clone https://www.github.com/nsorros/rasa-converter
pip install .[spacy,sklearn]
```

# ▶️ Quickstart

Train a spacy model using Rasa data

```
rasa-convert PATH_TO_RASA_DATA data.spacy --format spacy

spacy init config config.cfg --pipeline ner
spacy train config.cfg --paths.train data.spacy --paths.dev data.spacy
```

Train an sklearn model using Rasa data
```
rasa-convert PATH_TO_RASA_DATA data.jsonl

sklearn train data.jsonl
```
Note that we provide a convenient cli sklearn entrypoint
that trains a tfidf-svm model. You can write your own training
loop to experiment with different models.

# ⚙️ Contribute

You need to setup a development environment with all dependencies. You
also probably want to install the package in editable mode.

```
python -m venv venv
source venv/bin/activate

git clone https://www.github.com/nsorros/rasa-converter
pip install -e .[spacy,test]
```

To run tests run `pytest` or even better `tox`
