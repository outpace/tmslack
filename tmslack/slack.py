"""A tmslack-specific wrapper for the slack client."""
from pathlib import Path
from typing import Sequence

from slackclient import SlackClient

from tmslack.cache import Cache
from tmslack.config import Config


class ClientException(Exception):
    """Class for exceptions in the slack client."""


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
                raise ClientException(f'Failed to retrieve team information: {result["error"]}')
            return {k: result[k] for k in ['url', 'team', 'user', 'team_id', 'user_id']}

        self._info = teams_cache.get_through(token, lookup_team)
        self._user_cache = Cache(Path(cache_dir, f"{self._info['team_id']}_users"))

    @property
    def info(self):
        """Returns general information about the client.

        The returned map will have the url of the team, the team name, the bot name, the bot user
        identifier, and the team identifier.
        """
        return self._info

    def lookup_user_id(self, username) -> str:
        """Looks up a user identifier in the team by the user's name or real name."""
        def list_users(cursor=None):
            while True:
                result = self._slack.api_call('users.list', cursor=cursor)
                del result['headers']
                if not result['ok']:
                    raise IOError(f'Failed to list users: {result["error"]}')
                for member in result['members']:
                    yield member
                del result['members']
                cursor = result['response_metadata']['next_cursor']
                if cursor == "":
                    break

        def do_lookup_id(_):
            for user in list_users():
                if username == user.get('name') or username == user.get('real_name'):
                    return user['id']
            raise ClientException(f'The user {username} could not be found.')

        return self._user_cache.get_through(username, do_lookup_id)

    def lookup_conversation_id(self, user_ids: Sequence[str]) -> str:
        """Given a sequence of user names, get the identifier of the conversation between all those
        users."""
        result = self._slack.api_call('conversations.open', users=list(user_ids))
        if not result['ok']:
            raise ClientException(f'Failed to retrieve get conversation: {result["error"]}')

        return result['channel']['id']
