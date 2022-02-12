# -*- coding: utf-8 -*-


class BaseFrame(list):
    """ BaseFrame
    Base Field definded by the permutation of different field.

    Parameters
    ----------
    _construct_field: init method
        select field used
    _set_field: init method
        set field settings
    _construct_frame
        the order of field used

    Methods
    ----------
    _parse: method
        frame: frame list
        fields_out: select field to be parsed
        format_out: select output format
            - list: output as list
            - dict: output as dict
    """
    _kind = 'base'

    def __init__(self):
        super(BaseFrame, self).__init__()
        self.max_length = 20
        self._construct_field()
        self._set_field()
        self._construct_frame()

    def _construct_field(self):
        raise NotImplementedError

    def _set_field(self):
        raise NotImplementedError

    def _construct_frame(self):
        raise NotImplementedError

    def _parse(self, frame,
               fields_out=None,
               format_out='dict'):
        if not isinstance(frame, list):
            frame = list(frame)
        if not isinstance(fields_out, list):
            fields_out = [fields_out]
        fields_name_out = list(map(lambda field_out: field_out + ' field', fields_out))
        parsed = {'kind': self._kind}
        for field in self:
            block = frame[field.offset]
            field_parsed = field.parse(block)
            if field.name in fields_name_out:
                parsed[field.name[:-6]] = field_parsed
            # if format_out == 'dict':
            #     keys = ['kind'] + fields_out
            #     parsed = dict(zip(keys, parsed))
            if format_out == 'list':
                parsed = list(parsed.value())
        return parsed
    

        
        
        
        
        
        