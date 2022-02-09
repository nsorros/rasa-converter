import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("svm", SGDClassifier())
    ])
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)
    print(f1_score(y_test, y_pred, average="micro"))

if __name__ == "__main__":
    app()
