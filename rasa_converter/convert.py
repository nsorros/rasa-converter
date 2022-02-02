import glob
import yaml
import typer
import json
import re


app = typer.Typer()

def extract_entities(text):
    entities = []

    # note this finds the first match
    match = re.search(r"\[\w+\]\(\w+\)", text)
    if match:
        start_char, end_char = match.span()
        match_text = text[start_char:end_char]

        pattern = re.compile(r"\[(\w+)\]\((\w+)\)")
        entity_text, entity_label = pattern.findall(match_text)[0]

        text = text.replace(text[start_char:end_char], entity_text)    
        entities = [{"start_char": start_char, "end_char": start_char+len(entity_text), "label": entity_label, "text": entity_text}]
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
        from create_spacy_data import convert_to_spacy

        data = list(yield_data(input_path))
        spacy_data = convert_to_spacy(data)
        spacy_data.to_disk(output_path)
    else:
        print(f"format {format} not recognised") 

if __name__ == "__main__":
    app()
