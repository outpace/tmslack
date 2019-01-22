from pathlib import Path

import pytest
import yaml

from tmslack.config import load


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load('foo.bar')


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    return Path(tmp_path, 'config.yml')


def test_unreadable_config(config_file):
    config_file.touch(0o0200)
    with pytest.raises(PermissionError):
        load(config_file)


def test_malformed_config(config_file):
    config_file.write_text(':')
    with pytest.raises(yaml.YAMLError):
        load(config_file)


@pytest.fixture
def configure_with(config_file: Path):
    def _write_config(config) -> Path:
        with config_file.open('w') as out:
            yaml.dump(config, out)
        return config_file
    return _write_config


def test_empty_configuration(configure_with):
    config_file = configure_with(None)
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "Configuration must be a dictionary, found a NoneType."


def test_text_configuration(configure_with):
    config_file = configure_with("Foo!")
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "Configuration must be a dictionary, found a str."


def test_list_configuration(configure_with):
    config_file = configure_with([])
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "Configuration must be a dictionary, found a list."


def test_token_missing(configure_with):
    config_file = configure_with({})
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "No token found in the configuration."


def test_token_wrong_data_type(configure_with):
    config_file = configure_with({'token': 2})
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "The token must be a string, found a int."


def test_token_wrong_token_type(configure_with):
    config_file = configure_with({'token': 'xoxo'})
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "The token does not appear to be a bot token."


def test_token(configure_with):
    config_file = configure_with({'token': 'xoxb-42'})
    config = load(config_file)
    assert config.token == 'xoxb-42'
