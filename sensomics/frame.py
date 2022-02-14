# -*- coding: utf-8 -*-
from wearableio.frame import BaseFrame
from wearableio.sensomics.field import (HeadField, LengthField, KindField,
                                        UserField, DateField, DataField)
from wearableio.utils import (join_integer_decimal, join_byteblocks, join_complementary_byteblocks)
from pandas import Interval
from itertools import cycle
from datetime import datetime


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
    
    
### Record Frame
class RecordHRFrame(GenericFrame):
    """ RecordHRFrame
    RecordHRFrame (Recorded Heart Rate Frame) start with [171 0 255 81 17]

    Methods
    ----------
    parse: return unit /bpm
    """

    _kind = 'recordHR'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.date_field = DateField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x51)]}  # 255, 81
        self.user_field.settings = {'validator': [int(0x11)]}  # 17
        self.data_field.settings = {'size': 1,
                                    'offset': 11}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.date_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['date', 'data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class RecordSPO2Frame(GenericFrame):
    """ RecordSPO2Frame
    RecordSPO2Frame (Recorded SpO2 Frame) start with [171 0 255 81 18]

    Methods
    ----------
    parse: return unit /%
    """
    _kind = 'recordSPO2'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.date_field = DateField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x51)]}  # 255, 81
        self.user_field.settings = {'validator': [int(0x12)]}  # 18
        self.data_field.settings = {'size': 1,
                                    'offset': 11}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.date_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['date', 'data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class RecordSTFrame(GenericFrame):
    """ RecordSTFrame
    RecordSTFrame (Recorded Skin Temperature Frame) start with [171 0 255 81 19]

    Methods
    ----------
    parse: return floot, unit centigrade
    """
    _kind = 'recordST'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.date_field = DateField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x51)]}  # 255, 81
        self.user_field.settings = {'validator': [int(0x13)]}  # 19
        self.data_field.settings = {'size': 2,
                                    'offset': slice(11, 13)}
        self.data_field.parse_func = self.parse_data_field_func

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.date_field)
        self.append(self.data_field)

    @classmethod
    def parse_data_field_func(cls, blocks):
        integer = blocks[0]
        decimal = blocks[1]
        if decimal <= 100:
            decimal = decimal / 100
        else:
            raise ValueError('decimal value in %s' % (cls.__class__.__name__))
        parsed = integer + decimal
        return parsed

    def parse(self, frame,
              fields_out=['date', 'data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class RecordBPFrame(GenericFrame):
    """ RecordBPFrame
    RecordBPFrame (Recorded Blood Pressure Frame) start with [171 0 255 81 20]

    Methods
    ----------
    parse: return [high blood pressure, mmgh
                   low  blood pressure, mmgh]
    """
    _kind = 'recordBP'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.date_field = DateField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x51)]}  # 255, 81
        self.user_field.settings = {'validator': [int(0x14)]}  # 20
        self.data_field.settings = {'size': 2,
                                    'offset': slice(11, 13)}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.date_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['date', 'data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class RecordSleepFrame(GenericFrame):
    """ RecordSleepFrame
    RecordSleepFrame (Sleep Frame) start with [171 0 255 81 24]

    Methods
    ----------
    parse: return [sleep type, sleep minute]
    """
    _kind = 'recordSleep'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.date_field = DateField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x52)]}
        self.user_field.settings = {'validator': [int(0x80)]}  # 128
        self.data_field.settings = {'size': 3,
                                    'offset': slice(11, 14)}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.date_field)
        self.append(self.data_field)

    def parse_data_field_func(self, blocks):
        data0 = blocks[0]
        data1 = blocks[1: 3]
        sleep_type = data0
        sleep_time = join_byteblocks(data1, reverse=True)
        return [sleep_type, sleep_time]

    def parse(self, frame,
              fields_out=['date', 'data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)



### Statet Frame
class StateTagFrame(GenericFrame):
    """ StateTagFrame
    StateTagFrame (Tag Frame) start with [171 0 255 81 25]

    Methods
    ----------
    parse: return date
    """
    _kind = 'stateTag'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x51)]}  # 255, 81
        self.user_field.settings = {'validator': [int(0x18)]}  # 24
        self.data_field.settings = {'size': 6,
                                    'offset': slice(6, 12),
                                    'validator': [Interval(int(0x00), int(0xff), closed='both'),  # year [0,255]]
                                                  Interval(int(0x01), int(0x0c), closed='both'),  # month [1, 12]
                                                  Interval(int(0x01), int(0x1f), closed='both'),  # day [1, 31]
                                                  Interval(int(0x00), int(0x17), closed='both'),  # hour [0, 23]
                                                  Interval(int(0x00), int(0x3b), closed='both'),  # minute [0, 59]]
                                                  Interval(int(0x00), int(0x3b), closed='both'), ],  # second [0, 59]]
                                    }
        self.data_field.parse_func = self.parse_data_field_func

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    @classmethod
    def parse_data_field_func(cls, blocks):
        parsed = datetime(year=blocks[0] + 2000,
                          month=blocks[1],
                          day=blocks[2],
                          hour=blocks[3],
                          minute=blocks[4],
                          second=blocks[5])
        parsed = parsed.strftime("%Y-%m-%d-%H:%M:%S")
        return parsed

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StateMultiMeasureFrame(GenericFrame):
    """ StateMultiMeasureFrame
    StateMultiMeasureFrame (State Multi Measure Frame) start with [171 0 255 50 80]

    Methods
    ----------
    parse: return [heart rate,
                   SpO2,
                   [High Blood Pressure, Low Blood Pressure]
                   Skin Temperature]
    """

    _kind = 'stateMultiMeasure'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x32)]}  # 255, 50
        self.user_field.settings = {'validator': [int(0x80)]}
        self.data_field.parse_func = self.parse_data_field_func

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    @classmethod
    def parse_data_field_func(cls, blocks):
        data0 = blocks[0]
        data1 = blocks[1]
        data2 = blocks[2:4]
        data3 = blocks[5:7]
        hr = data0
        spo2 = data1
        bp = data2
        st = join_integer_decimal(data3)
        parsed = [hr, spo2, bp, st]
        return parsed

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StateActivityFrame(GenericFrame):
    """ StateActivityFrame
    StateActivityFrame (Activity Frame) start with [171 0 255 81 24]

    Methods
    ----------
    parse: return [step,
                   calorie,
                   Shallow Sleep time, unit minute
                   Deep Sleep time, unit minute
                   Wake Up number,
                   ]
    """
    _kind = 'stateActivity'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x51)]}
        self.user_field.settings = {'validator': [int(0x08)]}  # 24
        self.data_field.parse_func = self.parse_data_field_func

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse_data_field_func(self, blocks):
        data0 = blocks[0:3]
        data1 = blocks[3:6]
        data2 = blocks[6:8]
        data3 = blocks[8:10]
        data4 = blocks[10]
        step = join_byteblocks(data0, reverse=True)
        calorie = join_byteblocks(data1, reverse=True)
        shallow_sleep_minute = (lambda blocks: blocks[0] * 60 + blocks[1])(data2)
        deep_sleep_minute = (lambda blocks: blocks[0] * 60 + blocks[1])(data3)
        wake_up_time = data4
        return [step, calorie, shallow_sleep_minute, deep_sleep_minute, wake_up_time]

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StatePowerFrame(GenericFrame):
    _kind = 'statePower'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x91)]}
        self.user_field.settings = {'validator': [int(0x80)]}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StateBandInfoFrame(GenericFrame):
    _kind = 'stateBandInfo'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x92)]}
        self.user_field.settings = {'validator': [int(0xc0)]}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StateActivationFrame(GenericFrame):
    _kind = 'stateActivation'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x97)]}
        self.user_field.settings = {'validator': [int(0x80)]}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StateBandInfoExtendFrame(GenericFrame):
    _kind = 'stateBandInfoExtend'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x9b)]}
        self.user_field.settings = {'validator': [int(0x5)]}

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StateHRFrame(GenericFrame):
    _kind = 'stateHR'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x31)]}  # 255, 49
        self.user_field.settings = {'validator': [int(0x0a)]}  # 10

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)

    
    
### Stream Frame
Quantitativelevel = 12
So = 1/256

class StreamPPGFrame(BaseFrame):
    """ StreamPPGFrame
    StreamPPGFrame start with [171 0 17 29]
    attention: the size of kind_field is 1

    Methods
    ----------
    parse: return unit /bit

    """

    _kind = 'streamPPG'

    def _construct_field(self):
        # super(StreamPPGFrame, self)._construct_field()
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.data_field = DataField()

    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.length_field.settings = {'validator': [int(0x00), int(0x11)]}  # [0, 17]
        self.kind_field.settings = {'validator': [int(0x29)],
                                    'size': 1,
                                    'offset': 3}  # 41
        self.data_field.settings = {'size': 16,
                                    'offset': slice(4, 20)}

        self.data_field.parse_func = self.parse_data_field_func

    def _construct_frame(self):
        # super(StreamPPGFrame, self)._construct_frame()
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.data_field)

    @classmethod
    def parse_data_field_func(cls, blocks):
        data0 = blocks[0: 2]
        data1 = blocks[2: 4]
        data2 = blocks[4: 6]
        data3 = blocks[6: 8]
        data4 = blocks[8:10]
        data5 = blocks[10:12]
        data6 = blocks[12:14]
        data7 = blocks[14:16]
        parsed = list(map(lambda data: join_byteblocks(data),
                          [data0, data1, data2, data3, data4, data5, data6, data7]))
        return parsed

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)



class StreamACXFrame(BaseFrame):
    """ StreamACXFrame
    StreamACXFrame start with [161 0 10]
    indicate there are 5 groups 16bit data in data field

    Methods
    ----------
    parse: return unit /g
    """

    _kind = 'streamACX'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.data_field = DataField()

    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xa1)]}  # 161
        self.length_field.settings = {'validator': [int(0x00), int(0x0a)]}  # [0, 10]
        self.data_field.settings = {'size': 10,
                                    'offset': slice(3, 13)}

        self.data_field.parse_func = self.parse_data_field_func

    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.data_field)

    @classmethod
    def adc_to_physical(cls, value):
        # TODO: add notations:
        # https://www.geek-workshop.com/forum.php?mod=viewthread&tid=1695&reltid=676&pre_thread_id=0&pre_pos=1&ext=
        # https://blog.csdn.net/lovewubo/article/details/9084291
        # https://www.cnblogs.com/uestcman/p/9433871.html
        # low, high = value
        # adc = high << 8 | low
        adc = join_byteblocks(value)
        delta_voltage = adc / (2 ** Quantitativelevel - 1) * Vdd - Voff
        physical = delta_voltage / So  # unit g
        return physical

    @classmethod
    def complementary_to_physical(cls, value):
        adc = join_complementary_byteblocks(value)
        # digit = adc >> 6
        digit = adc
        physical = digit * So
        return physical

    @classmethod
    def parse_data_field_func(cls, blocks):
        data0 = blocks[0: 2]
        data1 = blocks[2: 4]
        data2 = blocks[4: 6]
        data3 = blocks[6: 8]
        data4 = blocks[8:10]
        parsed = list(map(lambda data: cls.complementary_to_physical(data),
                          [data0, data1, data2, data3, data4]))
        return parsed

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StreamACYFrame(BaseFrame):
    """ SteamACXFrame
    StreamACYFrame Frame start with [162 0 10]
    indicate there are 5 groups 16bit data in data field

    Methods
    ----------
    parse: return unit /g
    """

    _kind = 'streamACY'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.data_field = DataField()

    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xa2)]}  # 162
        self.length_field.settings = {'validator': [int(0x00), int(0x0a)]}  # [0, 10]
        self.data_field.settings = {'size': 10,
                                    'offset': slice(3, 13)}

        self.data_field.parse_func = self.parse_data_field_func

    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.data_field)

    @classmethod
    def adc_to_physical(cls, value):
        # TODO: add notations:
        # https://www.geek-workshop.com/forum.php?mod=viewthread&tid=1695&reltid=676&pre_thread_id=0&pre_pos=1&ext=
        # https://blog.csdn.net/lovewubo/article/details/9084291
        # https://www.cnblogs.com/uestcman/p/9433871.html
        # low, high = value
        # adc = high << 8 | low
        adc = join_byteblocks(value)
        delta_voltage = adc / (2 ** Quantitativelevel - 1) * Vdd - Voff
        physical = delta_voltage / So  # unit g
        return physical

    @classmethod
    def complementary_to_physical(cls, value):
        adc = join_complementary_byteblocks(value)
        # digit = adc >> 6
        digit = adc
        physical = digit * So
        return physical

    @classmethod
    def parse_data_field_func(cls, blocks):
        data0 = blocks[0: 2]
        data1 = blocks[2: 4]
        data2 = blocks[4: 6]
        data3 = blocks[6: 8]
        data4 = blocks[8:10]
        parsed = list(map(lambda data: cls.complementary_to_physical(data),
                          [data0, data1, data2, data3, data4]))
        return parsed

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StreamACZFrame(BaseFrame):
    """ SteamACXFrame
    StreamACZFrame start with [163 0 10]
    indicate there are 5 groups 16bit data in data field

    Methods
    ----------
    parse: return unit /g
    """

    _kind = 'streamACZ'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.data_field = DataField()

    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xa3)]}  # 163
        self.length_field.settings = {'validator': [int(0x00), int(0x0a)]}  # [0, 10]
        self.data_field.settings = {'size': 10,
                                    'offset': slice(3, 13)}
        self.data_field.parse_func = self.parse_data_field_func

    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.data_field)

    @classmethod
    def adc_to_physical(cls, value):
        # TODO: add notations:
        # https://www.geek-workshop.com/forum.php?mod=viewthread&tid=1695&reltid=676&pre_thread_id=0&pre_pos=1&ext=
        # https://blog.csdn.net/lovewubo/article/details/9084291
        # https://www.cnblogs.com/uestcman/p/9433871.html
        # low, high = value
        # adc = high << 8 | low
        adc = join_byteblocks(value)
        delta_voltage = adc / (2 ** Quantitativelevel - 1) * Vdd - Voff
        physical = delta_voltage / So  # unit g
        return physical

    @classmethod
    def complementary_to_physical(cls, value):
        adc = join_complementary_byteblocks(value)
        # digit = adc >> 6
        digit = adc
        physical = digit * So
        return physical

    @classmethod
    def parse_data_field_func(cls, blocks):
        data0 = blocks[0: 2]
        data1 = blocks[2: 4]
        data2 = blocks[4: 6]
        data3 = blocks[6: 8]
        data4 = blocks[8:10]
        parsed = list(map(lambda data: cls.complementary_to_physical(data),
                          [data0, data1, data2, data3, data4]))
        return parsed

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)


class StreamHRFrame(GenericFrame):
    """ StreamHRFrame
    StreamHRFrame start with [171 0 255 132 128] without date field

    Methods
    ----------
    parse: return unit /bpm
    """
    _kind = 'streamHR'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.head_field = HeadField()
        self.length_field = LengthField()
        self.kind_field = KindField()
        self.user_field = UserField()
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.head_field.settings = {'validator': [int(0xab)]}  # 171
        self.kind_field.settings = {'validator': [int(0xff), int(0x84)]}  # 255, 132
        self.user_field.settings = {'validator': [int(0x80)]}  # 128

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.head_field)
        self.append(self.length_field)
        self.append(self.kind_field)
        self.append(self.user_field)
        self.append(self.data_field)

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)

    

### Unknown Frame
class UnknownFrame(BaseFrame):
    _kind = 'unknown'

    def _construct_field(self):
        ''' Generic frame including 5 kind of fields '''
        self.data_field = DataField()

    # @Override
    def _set_field(self):
        self.data_field.settings = {'offset': slice(0, 20),
                                    'size': Interval(1, 20, closed='both'), }
        self.data_field.parse_func = self.parse_data_field_func

    # @Override
    def _construct_frame(self):
        ''' The order of the fields '''
        self.append(self.data_field)

    @classmethod
    def parse_data_field_func(cls, blocks):
        return blocks

    def parse(self, frame,
              fields_out=['data'],
              format_out='dict'):
        return self._parse(frame, fields_out, format_out)