# -*- coding: utf-8 -*-
"""
    matterllo
    ~~~~~~~~~

    The core application.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""
import logging
import os
import sys
from base64 import b64decode

from matterhook import Webhook
from flask import Flask
from flask import request
from slugify import slugify

from matterllo.parser import Parser
from matterllo.utils import config

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


app = Flask(__name__)
# NOTE: ugly way to load settings.
settings = config()
BEACON = b64decode('R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')


class Send(object):

    def __init__(self, parser, board, action, payload):
        """ Init the necessary stuff to sent the event.

        Args:
            parser (object): see matterllo/parser.py.
            board (str): the name board.
            action (dict): the trello action data.
            payload (str): the event payload.
        """
        self.parser = parser
        self.board = board
        self.action = action
        self.payload = payload

    def __call__(self):
        try:
            for key, values  in settings.get('boards', {}).items():
                board_name = slugify(values['name'])
                logging.info('{} :: {}'.format(self.board, board_name))
                if self.board != board_name:
                    continue
                
                for k, v in values['mattermost'].items():
                    if not self.allow_action(config=v):
                        logging.info('{} :: {} :: no subscribe for this event :: {}'.format(
                            key, v['channel'], self.action['type']))
                        continue

                    logging.info('{} :: send event to {}'.format(k, v['channel']))
                    mwh = Webhook(v['incoming_webhook_url'], v['incoming_webhook_key'])
                    mwh.username = v.get('username', 'Matterllo')
                    mwh.icon_url = v.get('icon_url', 'http://maffrigby.com/wp-content/uploads/2015/05/trello-icon.png')
                    mwh.send(self.payload, channel=v['channel'])
        except Exception as e:
            logging.error('unable to send payload :: {}'.format(e))

    def allow_action(self, config):
        """ There is the action into subscribe events list.

        Args:
            config (dict): The board configuration.
        """
        try:
            allow_actions = set()
            deny_actions = set()
            subscribe = config.get('subscribe', '*').replace(',', ' ').split(' ')

            if '*' in subscribe:
                allow_actions = {a.lower() for a in self.parser.supported_action}
    
            for action in subscribe:
                # NOTE: empty string due to split method.
                if not action or action == '*':
                    continue

                if action[0] == '-':
                    deny_actions.add(action[1:].lower())
                else:
                    allow_actions.add(action.lower())

            print allow_actions, deny_actions
            return self.action['type'].lower() in allow_actions.difference(deny_actions)
        except Exception as e:
            logging.error('unable to allow action :: {}'.format(e))

@app.route('/trelloCallbacks/', methods=['GET', 'POST'])
def callback():
    try:
        if request.method != 'POST':
            return BEACON

        data = request.json
        action = data['action']
        board = slugify(data['model']['name'])

        # NOTE: it's ugly to init for each request the parser class
        parser = Parser()
        payload = parser(action=action)

        if payload:
            send = Send(parser=parser, board=board, action=action, payload=payload)
            send()
    except KeyError as e:
        logging.error('missing necessary field :: {} :: {}'.format(e, data))
    except Exception as e:
        logging.error('unable to handle event :: {}'.format(e))
    finally:
        return BEACON
