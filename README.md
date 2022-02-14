# WearableIO
Python tools for parsering wearable frame byte stream .

## Introduction
WearableIO is a framework to add support for parsering wearable frame byte stream. 

The wearable frame is expressed as a set of byte stream. For example

1. `<0x00 0xA1 0x14 0x00 ...>`
2. `<0x00 0xA1 0x14 0x01 ...>`

The wearable frame protocol design these frames consisted of different types of fields, and each field combined several bytes. For example

Field name | Offset | Size | Value
---- | ----- | ------ | ---- 
Head Field | 0 | 2 | 0x00A1 
Length Field | 2 | 1 | 0x00 ~ 0x14
Type Field | 3 | 1 | 0x00 ~ 0xff
... | ... | ... | ...

With the pre-definded data protocol, the wearable frame would transfer to 

1. `<0x00 0xA1 0x14 0x00 ...>` -> `<Device Init1 Frame>`
2. `<0x00 0xA1 0x14 0x01 ...>` -> `<Device Init2 Frame>`
... ...

## Install
WearableIO depends on the following packages:
- `pandas`
- `collection`

## Example
### Define Protocol
```
from pandas import Interval
from itertools import cycle

DEFAULT_RANGE = Interval(int(0x00), int(0xff), closed='both')  # [0, 255]
SENSOMICS_FRAME_STRUCTURE = {
    'head_field': {'validator': [int(0xab)],
                   'offset': 0,
                   'size': 1},
    'length_field': {'validator': cycle([DEFAULT_RANGE]),
                     'offset': slice(1, 3),
                     'size': 2},
    'kind_field': {'validator': cycle([DEFAULT_RANGE]),
                   'offset': slice(3, 5),
                   'size': 2},
    'user_field': {'validator': cycle([DEFAULT_RANGE]),
                   'offset': 5,
                   'size': 1},
    'data_field': {'validator': cycle([DEFAULT_RANGE]),
                   'offset': slice(6, 20),
                   'size': Interval(1, 14, closed='both')}
}

SENSOMCIS_HEAD_FIELD_SETTINGS = {'name': 'head field',
                                 'size': 1,
                                 'validator': [int(0xab)],
                                 'offset': 0}
SENSOMCIS_LENGTH_FIELD_SETTINGS = {'name': 'length field',
                                   'size': 2,
                                   'validator': cycle([DEFAULT_RANGE]),
                                   'offset': slice(1, 3)}
SENSOMCIS_KIND_FIELD_SETTINGS = {'name': 'kind field',
                                 'size': 2,
                                 'validator': cycle([DEFAULT_RANGE]),
                                 'offset': slice(3, 5)}
SENSOMCIS_USER_FIELD_SETTINGS = {'name': 'user field',
                                 'size': 1,
                                 'validator': cycle([DEFAULT_RANGE]),
                                 'offset': 5}
SENSOMCIS_DATE_FIELD_SETTINGS = {'name': 'date field',
                                 'size': 5,
                                 'validator': [Interval(int(0x00), int(0xff), closed='both'),  # year [0,255]]
                                               Interval(int(0x01), int(0x0c), closed='both'),  # month [1, 12]
                                               Interval(int(0x01), int(0x1f), closed='both'),  # day [1, 31]
                                               Interval(int(0x00), int(0x17), closed='both'),  # hour [0, 23]
                                               Interval(int(0x00), int(0x3b), closed='both')],  # minute [0, 59]]
                                 'offset': slice(6, 11)}
SENSOMCIS_DATA_FIELD_SETTINGS = {'name': 'data field',
                                 'size': Interval(1, 14, closed='both'),
                                 'validator': cycle([DEFAULT_RANGE]),
                                 'offset': slice(6, 20)}
```



### Define Field
```
from datetime import datetime
from wearableio.field import BaseField

class HeadField(BaseField):
    """ HeadField """

    def __init__(self, **kwags):
        super(HeadField, self).__init__(**kwags)
        self.settings = SENSOMCIS_HEAD_FIELD_SETTINGS

    def parse(self, blocks):
        parsed = super().parse(blocks)
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed        

        

class LengthField(BaseField):
    """ LengthField """

    def __init__(self, **kwags):
        super(LengthField, self).__init__(**kwags)
        self.settings = SENSOMCIS_LENGTH_FIELD_SETTINGS

    def parse(self, blocks):
        parsed = super().parse(blocks)
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed



class KindField(BaseField):
    """ KindField """

    def __init__(self, **kwags):
        super(KindField, self).__init__(**kwags)
        self.settings = SENSOMCIS_KIND_FIELD_SETTINGS

    def parse(self, blocks):
        parsed = super().parse(blocks)
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed



class UserField(BaseField):
    """ UserField """

    def __init__(self, **kwags):
        super(UserField, self).__init__(**kwags)
        self.settings = SENSOMCIS_USER_FIELD_SETTINGS

    def parse(self, blocks):
        parsed = super().parse(blocks)
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed



class DataField(BaseField):
    """ DataField """

    def __init__(self, **kwags):
        super(DataField, self).__init__(**kwags)
        self.settings = SENSOMCIS_DATA_FIELD_SETTINGS

    def parse(self, blocks):
        parsed = super().parse(blocks)
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed
    
    

class DateField(BaseField):
    """ DateField """

    def __init__(self, **kwags):
        super(DateField, self).__init__(**kwags)
        self.settings = SENSOMCIS_DATE_FIELD_SETTINGS

    @classmethod
    def _parse_func(cls, blocks):
        ''' 
        datetime(year=block[0]+2000,
        month=block[1],
        day=block[2],
        hour=block[3],
        minute=block[4])
        '''
        blocks[0] = blocks[0] + 2000
        parsed = datetime(*blocks)
        parsed = parsed.strftime("%Y-%m-%d-%H:%M:%S")
        return parsed

    def parse(self, blocks):
        parsed = super().parse(blocks)
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed
```


### Define Frame
```
from wearableio.frame import BaseFrame

class GenericFrame(BaseFrame):
    """ GenericFrame
    Generic Frame definded the most commen field permutation in sensomics protocal.
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)
    """

    _kind = 'generic'

    # @Override
    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        pass

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)
        pass
```