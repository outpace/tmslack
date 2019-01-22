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


@pytest.fixture
def base_config():
    return {
        'token': 'xoxb-42',
        'user': 'dan'
    }


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


def test_token_missing(configure_with, base_config):
    del base_config['token']
    config_file = configure_with(base_config)
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "No token found in the configuration."


def test_token_wrong_data_type(configure_with, base_config):
    base_config['token'] = 2
    config_file = configure_with(base_config)
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "The token must be a string, found a int."


def test_token_wrong_token_type(configure_with, base_config):
    base_config['token'] = 'xoxo'
    config_file = configure_with(base_config)
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "The token does not appear to be a bot token."


def test_token(configure_with, base_config):
    config_file = configure_with(base_config)
    config = load(config_file)
    assert config.token == base_config['token']


def test_user_missing(configure_with, base_config):
    del base_config['user']
    config_file = configure_with(base_config)
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "No user found in the configuration."


def test_user_wrong_data_type(configure_with, base_config):
    base_config['user'] = 2
    config_file = configure_with(base_config)
    with pytest.raises(ValueError) as ei:
        load(config_file)
    assert str(ei.value) == "The user must be a string, found a int."


def test_user(configure_with, base_config):
    config_file = configure_with(base_config)
    config = load(config_file)
    assert config.user == base_config['user']
