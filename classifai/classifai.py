import json
import os

from autochat import ChatGPT

# read functions.json in same directory as this file
FOLDER = os.path.dirname(os.path.abspath(__file__))
FUNCTIONS_FILE = os.path.join(FOLDER, "functions.json")
TEMPLATE_FILE = os.path.join(FOLDER, "template.txt")

with open(FUNCTIONS_FILE) as f:
    functions_list = json.load(f)
    FUNCTIONS_SCHEMA = {f["name"]: f for f in functions_list}


class Classifier:
    def __init__(self, categories, instruction=None, strict_mode=True):
        """
        :param categories: List of categories to classify into
        :param instruction: Description of the objective
        :param strict_mode: If True, only classifies into the provided categories. If False, can suggest a new category.
        """
        self.categories = categories
        self.strict_mode = strict_mode
        self.classifyGPT = ChatGPT.from_template(TEMPLATE_FILE)
        self.classifyGPT.add_function(self.list_items, FUNCTIONS_SCHEMA["LIST_ITEMS"])
        self.classifyGPT.add_function(self.label_items, FUNCTIONS_SCHEMA["LABEL_ITEMS"])

        self.classifyGPT.context = "CATEGORIES: \n" + "\n".join(
            ["- " + c for c in categories]
        )
        if instruction:
            self.classifyGPT.context += f"\nINSTRUCTION: {instruction}\n"

        if self.strict_mode:
            self.classifyGPT.context += "MODE: classify"
        else:
            self.classifyGPT.context += "MODE: classify_or_create"

        self.classifyGPT.context += "\n---\n"

    def list_categories(self):
        # TODO: not used for now
        return self.categories

    def list_items(self, search=None):
        raise NotImplementedError

    def label_items(self, ids, label):
        raise NotImplementedError

    def classify(self):
        text = ""
        for _ in range(100):  # We don't like infinite loops
            for message in self.classifyGPT.run_conversation(text):
                print(">", message)
            # Ask user for response
            text = input("user:")
