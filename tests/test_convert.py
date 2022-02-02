import json
import os

from convert import convert


def read_jsonl(data_path):
    data = []
    with open(data_path) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def test_convert(tmp_path):
    input_path = os.path.join(os.path.dirname(__file__), "data/")
    output_path = tmp_path / "data.jsonl"
    convert(input_path, output_path)
    assert os.path.exists(output_path)

    data = read_jsonl(output_path)
    assert len(data) == 12
