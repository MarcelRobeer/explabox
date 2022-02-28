"""..."""


class ModelMixin:
    @property
    def is_classifier(self):
        return "classifier" in str(self.model.__class__).lower()


class IngestiblesMixin:
    def from_ingestibles(ingestibles, required=["data", "model", "labelprovider"]):
        for ingestible in required:
            if ingestible not in ingestibles:
                raise Exception(f"{ingestible} is required but not provided")
            exec(f'self.{ingestible} = ingestibles["{ingestible}"]')

    @property
    def ingestibles(self):
        elems = {}
        if hasattr(self, "data"):
            elems["data"] = self.data
        if hasattr(self, "model"):
            elems["model"] = self.model
        if hasattr(self, "labelprovider"):
            elems["labelprovider"] = self.labelprovider
        return elems
