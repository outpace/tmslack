"""Utilities for querying tmate."""
import subprocess


class TmateException(Exception):
    """Exception class for the tmate module."""


def ssh_connection():
    """Returns the current tmate SSH connection string."""
    result = subprocess.run(['tmate', 'display', '-p', "#{tmate_ssh}"],
                            text=True,
                            capture_output=True)
    if result.returncode != 0:
        raise TmateException('Failed to interact with tmate, are you in a tmate session?')
    ssh_string: str = result.stdout
    if not ssh_string.startswith('ssh'):
        raise TmateException('No ssh string returned, is the tmate session active?')
    return ssh_string.split(' ')[1].strip()
