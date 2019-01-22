"""A tmslack-specific wrapper for the slack client."""
from pathlib import Path

from slackclient import SlackClient

from tmslack.cache import Cache
from tmslack.config import Config


class Client:
    """"A slack client that can be used to send messages.

    Attributes:
        info: Generic information about the client
    """
    def __init__(self, configuration: Config, cache_dir):
        token = configuration.token
        self._slack = SlackClient(token)
        teams_cache = Cache(Path(cache_dir, 'teams'))

        def lookup_team(_):
            result = self._slack.api_call('auth.test')
            if not result['ok']:
                raise IOError('Failed to retrieve team information.')
            return {k: result[k] for k in ['url', 'team', 'user', 'team_id', 'user_id']}

        self._info = teams_cache.get_through(token, lookup_team)
        self._cache = Cache(Path(cache_dir, self._info.team_id))

    @property
    def info(self):
        """Returns general information about the client.

        The returned map will have the url of the team, the team name, the bot name, the bot user
        identifier, and the team identifier.
        """
        return self._info
