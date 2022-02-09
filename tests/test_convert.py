import json
import os

from spacy.tokens import DocBin
import spacy

from rasa_converter.convert import convert


def read_jsonl(data_path):
    data = []
    with open(data_path) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def read_spacy(data_path):
    docbin = DocBin()
    docbin.from_disk(data_path)

    nlp = spacy.blank("en")
    docs = docbin.get_docs(nlp.vocab)
    return docs

def test_convert(tmp_path):
    input_path = os.path.join(os.path.dirname(__file__), "data/")
    output_path = tmp_path / "data.jsonl"
    convert(input_path, output_path)
    assert os.path.exists(output_path)

    data = read_jsonl(output_path)
    assert len(data) == 12

def test_convert_spacy(tmp_path):
    input_path = os.path.join(os.path.dirname(__file__), "data/")
    output_path = tmp_path / "data.spacy"
    convert(input_path, output_path, format="spacy")
    assert os.path.exists(output_path)

    docs = read_spacy(output_path)
    assert len(list(docs)) == 12
