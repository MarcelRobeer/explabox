from string import printable, punctuation

import pytest
from instancelib import TextEnvironment
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from text_explainability.model import import_model

TEST_INSTANCES = list(printable)

TEST_LABELS = [
    ["punctuation"] if any(c in item for c in punctuation) else ["no_punctuation"] for item in TEST_INSTANCES
]

TEST_ENVIRONMENT = TextEnvironment.from_data(
    target_labels={"punctuation", "no_punctuation"},
    indices=list(range(len(TEST_INSTANCES))),
    data=TEST_INSTANCES,
    ground_truth=TEST_LABELS,
    vectors=None,
)

TEST_MODEL = import_model(
    model=Pipeline([("vect", HashingVectorizer()), ("nb", LogisticRegression())]), environment=TEST_ENVIRONMENT
)


@pytest.helpers.register
def DATA():
    """Helper: Example data for ingestible."""
    return TEST_ENVIRONMENT


@pytest.helpers.register
def MODEL():
    """Helper: Example model for ingestible."""
    return TEST_MODEL
