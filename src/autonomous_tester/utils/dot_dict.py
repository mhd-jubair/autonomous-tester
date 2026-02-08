"""Helper utility for accessing dictionary in dot notation."""


class DotDict(dict):
    """
    A dictionary subclass that supports attribute-style access.

    Allows accessing dictionary keys as attributes, and recursively converts nested dicts and lists of dicts.

    Example:
        d = DotDict({'a': 1, 'b': {'c': 2}, 'd': [{'e': 3}]})
        print(d.a)          # 1
        print(d.b.c)        # 2
        print(d.d[0].e)     # 3

        d.f = 4
        print(d['f'])       # 4
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the DotDict instance.

        Recursively converts nested dictionaries and lists of dictionaries
        into DotDict objects for attribute-style access.
        """
        super().__init__()
        data = dict(*args, **kwargs)
        for key, value in data.items():
            if isinstance(value, dict):
                value = DotDict(value)
            elif isinstance(value, list):
                value = [DotDict(v) if isinstance(v, dict) else v for v in value]
            self[key] = value

    def __getattr__(self, item):
        """
        Retrieve the value for a given attribute.

        Allows access to dictionary keys as attributes.
        Raises AttributeError if the key does not exist.
        """
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        """
        Set a value for a given attribute.

        Assigns the value to the corresponding dictionary key.
        """
        self[key] = value
