"""Maintains a cache in a file.

In general, the idea is that cache acts as a map.  However, any time a modification to the map
is made, it is immediately saved to disk.  The format of caches is considered an implementation
detail.
"""
from pathlib import Path

import pickle


def _ensure_cache_file(path: Path):
    """Ensures that a file exists at the given path.

    Raises:
        ValueError: if the path exists but is not a file
    """
    if path.exists():
        if not path.is_file():
            raise ValueError(f'{path} exists but is not a file.')
    else:
        path.parent.mkdir(mode=0o0750, parents=True, exist_ok=True)
        with path.open('xb') as stream:
            pickle.dump({}, stream)
        path.chmod(mode=0o0640)


class Cache:
    """A persistent cache that synchronizes the memory state with that of a file on disk.

    Attributes:
        path: the path where the cache is persisted(read-only)
    """
    def __init__(self, path):
        """Creates or opens a cache at the given path."""
        self._path = Path(path)
        _ensure_cache_file(self._path)
        self._load()

    @property
    def path(self) -> Path:
        """Returns the path to which the cache is persisted."""
        return self._path

    def get(self, key, default=None):
        """Gets the value of the key in the cache, or default if the key is not in the cache.

        Equivalent to::

            if cache.hask_key(key):
                return cache.get(key)
            else:
                return default

        Args:
            key: they key to extract from the cache
            default: the value to return if the key is not in the cache (defaults to None)
        """
        return self._data.get(key, default)

    def has_key(self, key):
        """Returns True if the cache holds the given key, otherwise False."""
        return key in self._data

    def __getitem__(self, item):
        return self._data[item]

    def set(self, key, value):
        """Sets the value of key to value.

        Equivalent to::

            cache[key] = value

        Note that this will save the value to the cache.
        """
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def get_through(self, key, or_else):
        """Returns the value of key from the cache or else calculate a value using or_else and
        save it in the cache.

        This function call is equivalent to::

            if cache.has_key(key):
                return cache.get(key)
            else:
                value = or_else(key)
                if value is not None:
                    cache.set(key, value)
                return value

        Args:
            key: the key to retrieve
            or_else: a function to call to get a value if the key is not present in the cache
        """
        if self.has_key(key):
            return self.get(key)
        value = or_else(key)
        if value is not None:
            self.__setitem__(key, value)
        return value

    def __repr__(self):
        return f'Cache({repr(self._path)})'

    def __str__(self):
        return str(self._data)

    def _load(self):
        """Loads the cache from disk and into the data attribute."""
        with self._path.open('rb') as stream:
            self._data = pickle.load(stream)

    def _save(self):
        """Loads the cache from disk and into the data attribute."""
        with self._path.open('wb') as stream:
            pickle.dump(self._data, stream)
