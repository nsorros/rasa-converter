import random
import json
import csv
import os

import typer

from rasa_converter.io import read_data, write_data

app = typer.Typer()


@app.command()
def split_data(data_path, train_data_path, test_data_path, test_size: float = 0.2, shuffle=True):
    _, format = os.path.splitext(data_path)

    data = read_data(data_path, format)

    if shuffle:
        random.shuffle(data)
    
    train_size = int(len(data)*(1-test_size))
    train_data = data[:train_size]
    test_data = data[train_size:]

    write_data(train_data, train_data_path, format)
    write_data(test_data, test_data_path, format)

if __name__ == "__main__":
    app()
