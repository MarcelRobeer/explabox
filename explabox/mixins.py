"""Extensions to classes."""


class ModelMixin:
    @property
    def is_classifier(self) -> bool:
        """Whether the included model is a classifier (True) or not (False)."""
        return "classifier" in str(self.model.__class__).lower()


class IngestiblesMixin:
    def check_requirements(self, elements=["data", "model"]) -> bool:
        """Check if the required elements are in the ingestibles.

        Args:
            elements (List[str], optional): Elements to check. Defaults to ['data', 'model'].

        Raises:
            ValueError: The required element is not in the ingestibles.

        Returns:
            bool: True if all requirements are included.
        """
        return self.ingestibles.check_requirements(elements)

    @property
    def data(self):
        """All data."""
        return self.ingestibles.data

    @property
    def labels(self):
        """Labelprovider."""
        return self.ingestibles.labels

    @property
    def labelset(self):
        """Names of labels."""
        return self.ingestibles.labelset

    @property
    def model(self):
        """Predictive model."""
        return self.ingestibles.model

    @property
    def splits(self):
        """Named splits."""
        return self.ingestibles.splits
