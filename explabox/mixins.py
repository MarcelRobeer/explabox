"""..."""


class ModelMixin:
    @property
    def is_classifier(self):
        return "classifier" in str(self.model.__class__).lower()


class IngestiblesMixin:
    def check_requirements(self, elements=['data', 'model']):
        return self.ingestibles.check_requirements(elements)

    @property
    def data(self):
        return self.ingestibles.data

    @property
    def labelprovider(self):
        return self.ingestibles.labelprovider

    @property
    def labels(self):
        return self.ingestibles.labels

    @property
    def model(self):
        return self.ingestibles.model

    @property
    def splits(self):
        return self.ingestibles.splits
