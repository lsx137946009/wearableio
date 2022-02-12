# -*- coding: utf-8 -*-


from pandas import Interval
from collections import Iterable



class BaseField:
    """ BaseField
    Base Field with several 8 bit blocks. Definded by the following parameters.

    Parameters
    ----------
    name : str
        Field name, recommend 'xxx field'
    size : int, Interval or Iterable
        Number of blocks allowed
    validator: Iterable
        Validator of blocks
    offset: int or slice
        Slice of each block
    settings: dict
        {'name': ,
         'size': ,
         'validator': ,
         'offset': ,}

    Notes
    ----------
    The following method should be overwrite if necessary.   
    parse_func(blocks) : set parse function, default return blocks itself
    clean(blocks) : default return function _clean(blocks) 
    
    Examples
    ----------
    >>> 
    
    """

    def __init__(self, name=None, size=None, validator=None, offset=None, settings=None):
        self.name = name
        self.size = size
        self.validator = validator
        self.offset = offset
        self._settings = settings

    @classmethod
    def _parse_func(cls, blocks):
        return blocks

    @property
    def parse_func(self):
        ''' Set parse function, default return block itself '''
        return self._parse_func

    @parse_func.setter
    def parse_func(self, parse_func):
        self._parse_func = parse_func

    @property
    def settings(self):
        settings = {}
        for setting in ['name', 'validator', 'size', 'offset']:
            settings[setting] = getattr(self, setting)
        self._settings = settings
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings
        for setting in settings:
            setattr(self, setting, settings[setting])

    def clean(self, blocks):
        if not isinstance(blocks, list):
            blocks = [blocks]  # convert element of size 1 to list
        ''' Field size validation '''
        if isinstance(self.size, Interval):
            if not len(blocks) in self.size:
                raise ValueError('Size of {} invalid: got {}, allow {} {}'.format(
                    self.__class__.__name__,
                    len(blocks),
                    type(self.size),
                    self.size))
        elif isinstance(self.size, int):
            if not len(blocks) == self.size:
                raise ValueError('Size of {} invalid: got {}, allow {} {}'.format(
                    self.__class__.__name__,
                    len(blocks),
                    type(self.size),
                    self.size))
        elif isinstance(self.size, Iterable):
            if not len(blocks) in self.size:
                raise ValueError('Size of {} invalid: got {}, allow {} {}'.format(
                    self.__class__.__name__,
                    len(blocks),
                    type(self.size),
                    self.size))
        else:
            raise ValueError('Size type of {} invalid: got {}, allow int, Interval or Iterable'.format(
                self.__class__.__name__,
                type(blocks)))
        ''' Field block validation '''
        if isinstance(self.validator, Iterable):
            if False in map(lambda val, validator:
                            (val in validator if isinstance(validator, Interval) else (val == validator)),
                            blocks, self.validator):
                raise ValueError('Blocks of {} invalid: got {}, allow {}'.format(
                    self.__class__.__name__,
                    blocks,
                    self.validator))
        else:
            raise ValueError('Validator of {} should be Iterable'.format(
                self.__class__.__name__))

    def parse(self, blocks):
        self.clean(blocks)
        parsed = self.parse_func(blocks)
        return parsed  
        






         