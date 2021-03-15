"""WordPress.org support forums fetcher."""

import logging
from typing import Callable, Generator, List, Union

import feedparser

from tap_wordpress_support_forums.cleaners import CLEANERS

API_SCHEME: str = 'https://'
API_BASE_URL: str = 'wordpress.org'
PATH_PLUGIN: str = '/support/plugin/:plugin:/feed'


class WordPressSupportForums(object):

    """WordPress Support Forum Entries """
    def __init__(self, plugins: Union[List[str], str]) -> None:
        """Initialize support forums api.

        Arguments:
            plugins {Union[List[str], str]} -- Name of the plugins
        """

        # Set plugin or plugins
        if isinstance(plugins, str):
            self.plugins = [plugins]
        else:
            self.plugins = plugins

    def support_requests(self) -> Generator:
        """Plugin Support Requests.

        Yields:
            Generator -- JSON
        """

        # Get the Cleaner
        cleaner: Callable = CLEANERS.get('support_requests', {})

        # For every plugin
        for plugin in self.plugins:
            path: str = f'{PATH_PLUGIN}' .replace(
                ':plugin:',
                plugin,
            )

            # Create the URL
            url: str = f'{API_SCHEME}{API_BASE_URL}{path}'

            logging.info(f'Loading: {url}')

            # Get the RSS feed
            SupportFeed = feedparser.parse(url)

            # Create a dict with the values from the RSS feed
            items: dict = [
                {
                    'id': entry.id,
                    'plugin': path,
                    'title': entry.title,
                    'published': entry.published,
                    'authors': entry.author,
                    'description': entry.description
                } for entry in SupportFeed.entries
            ]

            # Yield the items from the RSS feed
            yield from (
                cleaner(item)
                for item in items
            )
