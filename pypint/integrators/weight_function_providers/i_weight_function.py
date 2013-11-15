# coding=utf-8
"""

.. moduleauthor: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""


class IWeightFunction(object):
    def __init__(self):
        self.__weights = None

    def init(self, function):
        pass

    def evaluate(self, nodes):
        pass

    @property
    def weights(self):
        return self.__weights