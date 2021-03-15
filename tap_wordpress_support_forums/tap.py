"""WordPress Plugin Stats tap."""
# -*- coding: utf-8 -*-
import logging
from argparse import Namespace

import pkg_resources
from singer import get_logger, utils
from singer.catalog import Catalog

from tap_wordpress_support_forums.discover import discover
from tap_wordpress_support_forums.sync import sync
from tap_wordpress_support_forums.wordpress_support_forums import \
    WordPressSupportForums  # noqa: I001,E501; noqa: I001; noqa: I001

VERSION: str = pkg_resources.get_distribution(
    'tap-wordpress-support-forums',
).version
LOGGER: logging.RootLogger = get_logger()
REQUIRED_CONFIG_KEYS: tuple = ('plugins',)


@utils.handle_top_exception(LOGGER)
def main() -> None:
    """Run tap."""
    # Parse command line arguments
    args: Namespace = utils.parse_args(REQUIRED_CONFIG_KEYS)

    LOGGER.info(f'>>> Running tap-wordpress-support_forums v{VERSION}')

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog: Catalog = discover()
        catalog.dump()
        return

    # Otherwise run in sync mode
    if args.catalog:
        # Load command line catalog
        catalog = args.catalog
    else:
        # Loadt the  catalog
        catalog = discover()

    # Initialize WordPress client
    wp: WordPressSupportForums = WordPressSupportForums(args.config['plugins'])

    sync(wp, catalog)


if __name__ == '__main__':
    main()
