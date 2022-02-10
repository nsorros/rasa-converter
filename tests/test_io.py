import os

import pytest

from rasa_converter.io import read_data, write_data


def get_data(format):
    data_path = os.path.join(os.path.dirname(__file__), f"data/data.{format}")
    data = read_data(data_path, format=f".{format}")
    return data

@pytest.fixture
def jsonl_data():
    return get_data("jsonl")

@pytest.fixture
def csv_data():    
    return get_data("csv")

@pytest.fixture
def spacy_data():    
    return get_data("spacy")

def test_read_data_jsonl(jsonl_data):
    assert len(jsonl_data) == 12

def test_read_data_csv(csv_data):
    assert len(csv_data) == 12

def test_read_data_spacy(spacy_data):
    assert len(spacy_data) == 12

def test_write_data_jsonl(jsonl_data, tmp_path):
    output_path = tmp_path / "data.jsonl"
    write_data(jsonl_data, output_path, format=".jsonl")
    assert os.path.exists(output_path)    

    data = read_data(output_path, format=".jsonl")
    assert len(data) == 12

def test_write_data_csv(csv_data, tmp_path):
    format = "csv"
    output_path = tmp_path / "data.{format}"
    write_data(csv_data, output_path, format=f".{format}")
    assert os.path.exists(output_path)    

    data = read_data(output_path, format=f".{format}")
    assert len(data) == 12

def test_write_data_spacy(spacy_data, tmp_path):
    format = "spacy"
    output_path = tmp_path / "data.{format}"
    write_data(spacy_data, output_path, format=f".{format}")
    assert os.path.exists(output_path)    

    data = read_data(output_path, format=f".{format}")
    assert len(data) == 12
