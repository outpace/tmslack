"""Contains the stuff needed to manage configuration."""
from typing import NamedTuple

import yaml


class Config(NamedTuple):
    """Represents the configuration for the tmslack utility."""
    token: str


def __load_yaml(path) -> dict:
    """Loads the YAML at the given path, ensuring it is a dictionary."""
    with open(path, 'r') as stream:
        config_yaml = yaml.load(stream)
    if not isinstance(config_yaml, dict):
        typename = type(config_yaml).__name__
        raise ValueError(f'Configuration must be a dictionary, found a {typename}.')
    return config_yaml


def __get_token(config: dict) -> str:
    """Gets the token from the configuration, with some sanity checks."""
    if 'token' not in config:
        raise ValueError("No token found in the configuration.")
    token = config['token']
    if not isinstance(token, str):
        raise ValueError(f'The token must be a string, found a {type(token).__name__}.')
    if not token.startswith('xoxb-'):
        raise ValueError(f'The token does not appear to be a bot token.')
    return token


def load(path) -> Config:
    """Loads, validates, and returns the contents of the configuration file at the given path.

    Args:
        path: the path from which to load configuration

    Raises:
        FileNotFoundError: If the configuration file could not be found
        PermissionError: If the configuration file is unreadable
        yaml.YAMLError: If the configuration file cannot be parsed as valid YAML.
        ValueError: If the configuration is invalid for some other reason.
    """
    config = __load_yaml(path)
    token = __get_token(config)
    return Config(token)
