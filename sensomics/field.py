# -*- coding: utf-8 -*-

from datetime import datetime
from wearableio.field import BaseField
from wearableio.sensomics.settings import (
    SENSOMCIS_HEAD_FIELD_SETTINGS,
    SENSOMCIS_LENGTH_FIELD_SETTINGS,
    SENSOMCIS_KIND_FIELD_SETTINGS,
    SENSOMCIS_USER_FIELD_SETTINGS,
    SENSOMCIS_DATA_FIELD_SETTINGS,
    SENSOMCIS_DATE_FIELD_SETTINGS)


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