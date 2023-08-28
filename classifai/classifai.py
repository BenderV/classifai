import csv
import json
import os

from autochat import ChatGPT, ContextLengthExceededError

# read functions.json in same directory as this file
FOLDER = os.path.dirname(os.path.abspath(__file__))
FUNCTIONS_FILE = os.path.join(FOLDER, "functions.json")
TEMPLATE_FILE = os.path.join(FOLDER, "template.txt")

with open(FUNCTIONS_FILE) as f:
    functions_list = json.load(f)
    FUNCTIONS_SCHEMA = {f["name"]: f for f in functions_list}


class Classifier:
    def __init__(
        self,
        data,
        categories,
        category_column="category",
        instruction=None,
        strict_mode=True,
    ):
        """
        :param categories: List of categories to classify into
        :param instruction: Description of the objective
        :param strict_mode: If True, only classifies into the provided categories. If False, can suggest a new category.
        """
        self.data = data

        # add id column if not present
        if "id" not in self.data[0]:
            for i, row in enumerate(self.data):
                row["id"] = i

        self.category_column = category_column
        # if category_column not in self.data, add it
        if category_column not in self.data[0]:
            for row in self.data:
                row[category_column] = None

        self.categories = categories
        self.strict_mode = strict_mode
        self.classifyGPT = ChatGPT.from_template(TEMPLATE_FILE)
        self.classifyGPT.add_function(self.list_items, FUNCTIONS_SCHEMA["LIST_ITEMS"])
        self.classifyGPT.add_function(
            self.update_items_category, FUNCTIONS_SCHEMA["UPDATE_ITEMS_CATEGORY"]
        )
        self.classifyGPT.add_function(
            self.list_categories, FUNCTIONS_SCHEMA["LIST_CATEGORIES"]
        )

        self.classifyGPT.context = "CATEGORIES: \n" + "\n".join(
            ["- " + c for c in categories]
        )
        if instruction:
            self.classifyGPT.context += f"\nINSTRUCTION: {instruction}\n"

        if self.strict_mode:
            self.classifyGPT.context += "MODE: classify"
        else:
            self.classifyGPT.add_function(
                self.create_category, FUNCTIONS_SCHEMA["CREATE_CATEGORY"]
            )
            self.classifyGPT.context += "MODE: classify_or_create"

    def list_categories(self, search=None):
        if search:
            return [c for c in self.categories if search in c]
        return self.categories

    def create_category(self, name):
        self.categories.append(name)
        return f"Created category {name}"

    def list_items(self, search=None, with_category=False, offset=0, limit=None):
        """
        - search: "The keyword to be searched for. If None, all data will be listed.
        - with_category: If True, only list data with a category. If False, only list data without a category.
        - limit: The maximum number of data to be listed.
        """

        if with_category:
            rows = [row for row in self.data if row[self.category_column]]
        else:
            # Otherwise, list all data without a category
            rows = [row for row in self.data if not row[self.category_column]]

        # If a search term is specified, search in any of the columns
        if search:
            rows = [
                row
                for row in rows
                if any([search.lower() in str(row[col]).lower() for col in row])
            ]

        # Handle offset and limit
        if offset:
            rows = rows[offset:]
        if limit:
            rows = rows[:limit]
        return rows

    def update_items_category(self, ids, category):
        """
        Label the items with the provided IDs with the provided label.
        """
        if category not in self.categories:
            raise ValueError(f"Category {category} does not exist.")
        for item in self.data:
            if str(item["id"]) in ids:
                item[self.category_column] = category
        self.on_data_update()

        categorized = [item for item in self.data if item[self.category_column]]
        return f"Updated {len(ids)} items to {category}.\nStats: {len(categorized)} / {len(self.data)} items categorized."

    def on_data_update(self):
        """
        Called when the data is changed.
        """
        pass

    def cli(self):
        text = ""
        for _ in range(100):  # We don't like infinite loops
            try:
                for message in self.classifyGPT.run_conversation(text):
                    print(message.to_markdown())
                # Ask user for response
                text = input("## user\n")
                if not text:
                    break
            except ContextLengthExceededError:
                print("Context length exceeded. Resetting history.")
                self.classifyGPT.reset_history()
                text = ""


class CSVClassifier(Classifier):
    def __init__(self, *args, csv_path=None, **kwargs):
        self.csv_path = csv_path
        data = self.read_csv()
        super().__init__(*args, data=data, **kwargs)

    def read_csv(self):
        with open(self.csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows

    def write_csv(self):
        with open(self.csv_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)

    def on_data_update(self):
        self.write_csv()

    def cli(self):
        return super().cli()
