# -*- coding: utf-8 -*-
"""
    matterllo.hook
    ~~~~~~~~~~~~~~

    The application to parse card action.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

class BaseHook(object):

    @classmethod
    def actions(cls):
        """ Returns all supported actions.
        """
        return [m for m in cls.__dict__ if not '__' in m]
