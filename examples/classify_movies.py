from classifai import CSVClassifier

categories = ["HORROR", "COMEDY", "ROMANCE", "ACTION"]
instruction = """Classify all the films into one of the categories above."""

ai = CSVClassifier(
    categories=categories,
    instruction=instruction,
    strict_mode=False,
    csv_path="movies.csv",
)
ai.classify()
