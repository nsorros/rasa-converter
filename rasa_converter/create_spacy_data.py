from spacy.tokens import DocBin
import spacy
import typer
import json


def convert_to_spacy(examples):
    nlp = spacy.blank("en")
    doc_bin = DocBin()
    for example in examples:
        doc = nlp(example["text"])

        doc.ents = [
            doc.char_span(ent["start_char"], ent["end_char"], label=ent["label"], alignment_mode="expand")
            for ent in example["entities"]
        ]
        doc.cats[example["intent"]] = 1.0
        doc_bin.add(doc)
    return doc_bin

def create_spacy_data(data_path, spacy_data_path):
    examples = []
    with open(data_path) as f:
        for line in f:
            examples.append(json.loads(line))

    spacy_data = convert_to_spacy(examples)
    spacy_data.to_disk(spacy_data_path)

if __name__ == "__main__":
    typer.run(create_spacy_data)
