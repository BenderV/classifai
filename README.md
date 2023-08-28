# Classifai - WIP

This package provides a text classification system that uses OpenAI's ChatGPT model to classify text into specified categories.

The classifier can be used in strict mode, which only classifies into the provided categories, or in non-strict mode, where it can suggest a new category if none of the provided ones fit.

## Installation

```
pip install classifai
```

## Usage

The main class in this package is `Classifier`. Here's how you can use it:

```python
from classifai import Classifier

categories = ['Category 1', 'Category 2', 'Category 3']
classifier = Classifier(categories, instruction="Classify the following items", strict_mode=True)

# To classify text
classifier.cli()
```

### Classifier Parameters

- `categories`: List of categories to classify into.
- `instruction`: Description of the objective (optional).
- `strict_mode`: If True, only classifies into the provided categories. If False, can suggest a new category (default is True).

### Methods

- `list_categories()`: Returns the list of categories. This method is not used for now.
- `list_items(search=None)`: This method should be implemented to return the items to be classified.
- `update_items_category(ids, category)`: This method should be implemented to handle the categorization of classified items.
- `classify()`: Starts the classification process. It repeatedly generates messages from the ChatGPT model and waits for user input.

## Dependencies

This package depends on the [autochat](https://github.com/BenderV/autochat) library.

## License

This project is licensed under the terms of the MIT license.
