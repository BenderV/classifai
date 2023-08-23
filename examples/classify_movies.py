import csv

from classifai import Classifier


class CSVClassifier(Classifier):
    def __init__(self, *args, csv_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_path = csv_path

    def list_items(self, search: str = None) -> str:
        with open(self.csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # Filter rows
            print("search", search)
            if search:
                rows = [row for row in rows if search in row["LIBUNI"]]

            if not rows:
                return "No items found"
            return rows

    def label_items(self, ids: str, label: str):
        if "," in ids:
            ids = ids.split(",")
        else:
            ids = [ids]

        with open(self.csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            if row["id"] in ids:
                row["category"] = label

        with open(self.csv_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        # Return the number of items labeled
        return "Labeled {} items".format(len(ids))


categories = ["HORROR", "COMEDY", "ROMANCE", "ACTION"]
instruction = """Classify the following films into one of the categories above."""

ai = CSVClassifier(
    categories=categories,
    instruction=instruction,
    strict_mode=False,
    csv_path="movies.csv",
)

ai.classify()
