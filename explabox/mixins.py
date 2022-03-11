"""Extensions to classes."""


class ModelMixin:
    @property
    def is_classifier(self) -> bool:
        """Whether the included model is a classifier (True) or not (False)."""
        return "classifier" in str(self.model.__class__).lower()


class IngestiblesMixin:
    def check_requirements(self, elements=["data", "model"]):
        """Check whether the ingestibles adheres to the requirements.

        Args:
            elements (list, optional): Elements that should be included. Defaults to ["data", "model"].

        Returns:
            _type_: _description_
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
