import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
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
    print("💾 Loading data")
    X, y = load_data(data_path)

    print("🪓 Splitting data")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    print("🤖 Training model")
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("svm", SGDClassifier())
    ])
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)
    p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="micro")

    print()
    print("📈 Results")
    print("-"*20)
    print(f"P {p:.2f} R {r:.2f} f1 {f1:.2f}")

if __name__ == "__main__":
    app()
