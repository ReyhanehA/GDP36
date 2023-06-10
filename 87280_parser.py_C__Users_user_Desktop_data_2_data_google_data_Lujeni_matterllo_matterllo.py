# -*- coding: utf-8 -*-
"""
    matterllo.parser
    ~~~~~~~~~~~~~~~~

    The application to parse each action.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""
from trello import TrelloClient

from matterllo.hook.card import Hook as HookCard
from matterllo.hook.list import Hook as HookList
from matterllo.hook.checklist import Hook as HookChecklist
from matterllo.utils import logger
from matterllo.utils import config

LOGGING = logger()
SETTINGS = config()


class Parser(HookCard, HookList, HookChecklist):

    def __init__(self):
        self.supported_action = HookCard.actions() + HookList.actions() + HookChecklist.actions()
        self.trello_client = TrelloClient(api_key=SETTINGS['trello_api_key'], token=SETTINGS['trello_api_token'])

    def __call__(self, action):
        """ Parse the event/action and return a pretty output.

        Args:
            action (dict): the trello action data.
        """
        try:
            action_type = action['type']
            if action_type not in self.supported_action:
                raise NotImplementedError(action_type)

            action_parser = getattr(self, action_type)
            return action_parser(action=action)
        except NotImplementedError as e:
            LOGGING.info('action parsing not implemented :: {}'.format(e))
        except Exception as e:
            LOGGING.error('unable to parse the action :: {} :: {}'.format(e, action))
