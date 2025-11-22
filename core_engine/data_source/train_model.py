import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_model():
    df = pd.read_csv('psychological_state_dataset.csv')

    X = df[['HRV (ms)', 'GSR (μS)']]
    y = df['Psychological State']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    joblib.dump(clf, 'sensemind_model.pkl')


if __name__ == "__main__":
    train_model()