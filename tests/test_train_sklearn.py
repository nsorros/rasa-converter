import os

from rasa_converter.train_sklearn import train


def test_train():
    data_path = os.path.join(os.path.dirname(__file__), "data/data.jsonl")
    train(data_path)
