import pickle
from pathlib import Path

import pytest

from tmslack.cache import Cache


def test_init_new_file(tmp_path):
    cache_file = Path(tmp_path, 'cache.yml')
    cache = Cache(cache_file)
    assert cache_file.exists()
    assert cache._path == cache_file
    assert cache._data == {}
    assert repr(cache) == f"Cache({repr(cache_file)})"
    assert str(cache) == str(cache._data)


def test_init_with_directory(tmp_path):
    with pytest.raises(ValueError) as ei:
        Cache(tmp_path)
    assert str(ei.value) == f'{tmp_path} exists but is not a file.'


def test_init_new_file_with_parent_directories(tmp_path):
    cache_file = Path(tmp_path, 'a', 'b', 'c', 'cache.yml')
    cache = Cache(cache_file)
    assert cache_file.exists()
    assert cache._path == cache_file
    assert cache._data == {}
    assert repr(cache) == f"Cache({repr(cache_file)})"
    assert str(cache) == str(cache._data)


@pytest.fixture
def cache(tmp_path):
    cache_file = Path(tmp_path, 'cache.yml')
    with cache_file.open('wb') as stream:
        pickle.dump({'a': 1, 'b': 2, 'c': 3}, stream)
    return Cache(cache_file)


def unpickle(cache):
    with cache._path.open('rb') as stream:
        return pickle.load(stream)


def test_get(cache):
    assert cache.get('a') == 1
    assert cache.get('b') == 2
    assert cache.get('c') == 3
    assert cache.get('d') is None
    assert cache.get('d', 'pizza') == 'pizza'


def test_has_key(cache):
    assert cache.has_key('a')
    assert cache.has_key('b')
    assert cache.has_key('c')
    assert not cache.has_key('d')


def test_getitem(cache):
    assert cache['a'] == 1
    assert cache['b'] == 2
    assert cache['c'] == 3
    with pytest.raises(KeyError):
        assert cache['d'] == 4


def test_setitem(cache):
    cache['a'] = 'foo'
    assert cache['a'] == 'foo'
    assert cache._data == {'a': 'foo', 'b': 2, 'c': 3}
    assert unpickle(cache) == cache._data
    cache['d'] = 4
    assert cache['d'] == 4
    assert cache._data == {'a': 'foo', 'b': 2, 'c': 3, 'd': 4}
    assert unpickle(cache) == cache._data


def test_set(cache):
    cache.set('a', 'foo')
    assert cache['a'] == 'foo'
    assert cache._data == {'a': 'foo', 'b': 2, 'c': 3}
    assert unpickle(cache) == cache._data
    cache.set('d', 4)
    assert cache['d'] == 4
    assert cache._data == {'a': 'foo', 'b': 2, 'c': 3, 'd': 4}
    assert unpickle(cache) == cache._data


def test_get_through(cache):
    def or_else(_):
        return 'from lambda'
    assert cache.get_through('a', or_else) == 1
    assert cache.get_through('d', or_else) == 'from lambda'
    assert cache['d'] == 'from lambda'
    assert cache._data == {'a': 1, 'b': 2, 'c': 3, 'd': 'from lambda'}
    assert unpickle(cache) == cache._data


def test_get_through_with_none(cache):
    def or_else(_):
        return None
    assert cache.get_through('a', or_else) == 1
    assert cache.get_through('d', or_else) is None
    assert not cache.has_key('d')
    assert cache._data == {'a': 1, 'b': 2, 'c': 3}
    assert unpickle(cache) == cache._data
