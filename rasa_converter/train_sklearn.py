import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import typer

app = typer.Typer()


def load_data(data_path):
    data = []
    with open(data_path) as f:
        for line in f:
            item = json.loads(line)
            data.append((item["text"], item["intent"]))

    X, y = zip(*data)
    return X, y

@app.command()
def train(data_path):
    X, y = load_data(data_path)
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("svm", SGDClassifier())
    ])
    model.fit(X,y)

    print(model.score(X,y))

if __name__ == "__main__":
    app()
