__all__ = ["NULL_DICT"]

from collections.abc import Mapping


class NullDict(Mapping):
    """A read-only empty dict-like class to be safely used as default argument."""

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])

    def __getitem__(self, key):
        return None

    def __setitem__(self, key, value):
        pass

    def __contains__(self, key):
        return False


"""A singleton instance of NullDict."""

NULL_DICT = NullDict()
