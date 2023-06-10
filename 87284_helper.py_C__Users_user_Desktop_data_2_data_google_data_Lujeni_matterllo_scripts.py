# -*- coding: utf-8 -*-
"""
    scripts.init_webhook
    ~~~~~~~~~~~~~~~~~~~~

    A simple script to manage the webhook.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""
import argparse
import sys

from trello import TrelloClient
from slugify import slugify

from matterllo.utils import config
from matterllo.utils import logger

SETTINGS = config()
LOGGING = logger()


def main():
    try:
        parser = argparse.ArgumentParser(description="Webhook helpers")
        parser.add_argument('--cleanup', dest='cleanup', action='store_true', help='delete webhook from your SETTINGS.')
        parser.add_argument('--update', dest='update', action='store_true', help='upsert webhook from your SETTINGS.')
        parser.add_argument('--init', dest='init', action='store_true', help='delete and create webhook from your SETTINGS.')

        args = parser.parse_args()
        if not args.cleanup and not args.update and not args.init:
            print parser.print_help()
            sys.exit(0)

        client = TrelloClient(api_key=SETTINGS['trello_api_key'], token=SETTINGS['trello_api_token'])
        trello_boards = client.list_boards()

        boards_name = [slugify(b['name']) for b in SETTINGS.get('boards', {}).values()]

        # cleanup part
        if args.cleanup or args.init:
            result = [h.delete() for h in client.list_hooks()]
            LOGGING.info('delete {} webhook'.format(len(result)))

        # update / init part
        if args.update or args.init:
            for board in trello_boards:
                board_name = slugify(board.name)
                if board_name not in boards_name:
                    continue

                LOGGING.info('try to create webhook board :: {}'.format(board_name))
                url = SETTINGS['callback_url'] + '/trelloCallbacks/'
                result = client.create_hook(url, board.id)
                LOGGING.info('create webhook board :: {} :: {}'.format(board_name, result))
    except Exception as e:
        LOGGING.error('unable init webhook :: {}'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
