"""Provides the main entry point for the tmslack utility."""
from pathlib import Path

import click
import xdg

from tmslack import config, slack

DEFAULT_CACHE_DIRECTORY = str(Path(xdg.XDG_CACHE_HOME, 'tmslack'))
DEFAULT_CONFIG_PATH = str(Path(xdg.XDG_CONFIG_HOME, 'tmslack', 'config.yml'))


@click.command(help='Invites a fellow slack user to your tmate.')
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
def main(config_file, cache_directory):
    """Does all of the actual work."""
    configuration = config.load(config_file)
    client = slack.Client(configuration, cache_directory)
    print(client.info)
