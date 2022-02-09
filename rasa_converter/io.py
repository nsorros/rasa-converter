import json
import csv


def read_data(data_path, format):
    data = []
    if format == ".jsonl":
        with open(data_path) as f:
            for line in f:
                data.append(json.loads(line))
    elif format == ".csv":
        with open(data_path) as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                data.append(row)
    elif format == ".spacy":
        from spacy.tokens import DocBin
        import spacy

        nlp = spacy.blank("en")
        docbin = DocBin().from_disk(data_path)
        data = list(docbin.get_docs(nlp.vocab))
    else:
        raise Exception(f"format {format} not recognised")
    return data

def write_data(data, data_path, format):
    if format == ".jsonl":
        with open(data_path, "w") as f:
            for item in data:
                f.write(json.dumps(item))
                f.write("\n")
    elif format == ".csv":
        with open(data_path, "w") as f:
            first_item = data[0]
            fieldnames = first_item.keys()

            csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
            csvwriter.writeheader()
            for row in data:
                csvwriter.writerow(row)
    elif format == ".spacy":
        from spacy.tokens import DocBin

        docbin = DocBin()
        for doc in data:
            docbin.add(doc)
        docbin.to_disk(data_path)
    else:
        raise Exception(f"format {format} not recognised")
