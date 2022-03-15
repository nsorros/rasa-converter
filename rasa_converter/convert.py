import glob
import yaml
import typer
import json
import csv
import ast
import re


app = typer.Typer()


def extract_entities(text):
    entities = []

    # [entity-text](entity-label)
    match = re.search(r"\[([a-zA-Z ]+)\]\((\w+)\)", text)
    while match:
        start_char, end_char = match.span()
        match_text = match.group(0)

        entity_text, entity_label = match.group(1), match.group(2)

        text = text.replace(match_text, entity_text)
        entities.append({"start_char": start_char, "end_char": start_char+len(entity_text), "label": entity_label, "text": entity_text})

        match = re.search(r"\[([a-zA-Z ]+)\]\((\w+)\)", text)
    
    # [entity-text]{entity-dict}
    match = re.search(r"\[([a-zA-Z ]+)\](\{[a-z\:\", ]+\})", text)
    while match:
        start_char, end_char = match.span()
        match_text = match.group(0)

        entity_text = match.group(1)
        entity_data = ast.literal_eval(match.group(2))
        entity_label = entity_data["entity"]

        text = text.replace(match_text, entity_text)
        entities.append({"start_char": start_char, "end_char": start_char+len(entity_text), "label": entity_label, "text": entity_text})

        match = re.search(r"\[([a-zA-Z ]+)\](\{[a-z\:\", ]+\})", text)

    return text, entities

def yield_data(input_path):
    nlus = glob.glob(input_path + "/**/nlu.yml", recursive=True)
    
    for nlu in nlus:
        print(f"Processing {nlu}")
        with open(nlu) as f:
            nlu_data = yaml.safe_load(f)

        for intent_data in nlu_data["nlu"]:
            # synonyms ignored for example
            if "intent" not in intent_data:
                continue

            # Split multiline string |
            examples = intent_data["examples"].split("\n")
            for example in examples:
                if not example: # skip empty line
                    continue
                text = example[2:] # skip "- "
                text, entities = extract_entities(text)
                yield {"text": text, "intent": intent_data["intent"], "entities": entities}

@app.command()
def convert(input_path, output_path, format="jsonl"):
    if format=="jsonl":
        with open(output_path, "w") as f:
           for item in yield_data(input_path):
                f.write(json.dumps(item)+"\n")
    elif format == "spacy":
        from rasa_converter.create_spacy_data import convert_to_spacy

        data = list(yield_data(input_path))
        spacy_data = convert_to_spacy(data)
        spacy_data.to_disk(output_path)
    elif format == "csv":
        with open(output_path, "w") as f:
            fieldnames = ["text", "intent"]
            csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
            
            csvwriter.writeheader()
            for item in yield_data(input_path):
                item.pop("entities")
                csvwriter.writerow(item)
        
    else:
        print(f"format {format} not recognised") 

if __name__ == "__main__":
    app()
