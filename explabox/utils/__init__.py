"""Utility functions and classes."""

from .io import create_output_dir


class MultipleReturn:
    """Holds multiple return values (e.g. from `return_types`) in one iterable return value."""

    def __init__(self, *return_values):
        self.return_values = return_values

    def _repr_html_(self):
        return "".join(v._repr_html_() for v in self.return_values)

    def __repr__(self):
        return repr(self.return_values)

    def __str__(self):
        return str(self.return_values)

    def __getitem__(self, i):
        return self.return_values[i]

    def __len__(self):
        return len(self.return_values)

    def to_config(self):
        if len(self.return_values) == 1:
            return self.return_values[0].to_config()
        return [v.to_config() for v in self.return_values]
