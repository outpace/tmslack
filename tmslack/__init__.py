"""Provides the main entry point for the tmslack utility."""
from pathlib import Path
from typing import Tuple

import click
import xdg

from tmslack import config, slack, tmate

DEFAULT_CACHE_DIRECTORY = str(Path(xdg.XDG_CACHE_HOME, 'tmslack'))
DEFAULT_CONFIG_PATH = str(Path(xdg.XDG_CONFIG_HOME, 'tmslack', 'config.yml'))


@click.command(help='Invites fellow slack users to your tmate.')
@click.option('--config-file',
              default=DEFAULT_CONFIG_PATH,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='The path to the configuration file.',
              show_default=True)
@click.option('--cache-directory',
              type=click.Path(exists=False, file_okay=False, dir_okay=True),
              default=DEFAULT_CACHE_DIRECTORY,
              help='The path to the cache directory.',
              show_default=True)
@click.argument('user', nargs=-1, type=str)
def main(config_file: str, cache_directory: str, user: Tuple[str, ...]):
    """Does all of the actual work."""
    configuration = config.load(config_file)
    client = slack.Client(configuration, cache_directory)
    ssh_connection = tmate.ssh_connection()
    print(ssh_connection)
    return 0
