# -*- coding: utf-8 -*-

from pandas import Interval
from itertools import cycle
# from wearableio.sensomics.frame import (
#     StreamHRFrame, StreamPPGFrame, StreamACXFrame, StreamACYFrame, StreamACZFrame,
#     RecordHRFrame, RecordSPO2Frame, RecordBPFrame, RecordSTFrame, RecordSleepFrame,
#     StateTagFrame, StateHRFrame, StateActivityFrame, StateMultiMeasureFrame,
#     StateActivationFrame, StatePowerFrame, StateBandInfoFrame, StateBandInfoExtendFrame)


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

SENSOMICS_FRAME_EXTEND_STRUCTURE = {
    'head_field': {'validator': [int(0x00)],
                   'offset': 0,
                   'size': 1},
    'length_field': {'validator': cycle([DEFAULT_RANGE]),
                     'offset': slice(1, 3),
                     'size': 2},
    'extend_data_field': {'validator': cycle([DEFAULT_RANGE]),
                          'offset': slice(3, 20),
                          'size': Interval(1, 19, closed='both')}
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



# =============================================================================
# ### SENSOMICS_FRAME_TYPE
# SENSOMICS_FRAME_TYPE = {
#     0xa1: StreamACXFrame(),  # 'streamACX'
#     0xa2: StreamACYFrame(),  # 'streamACY'
#     0xa3: StreamACZFrame(),  # 'streamACZ'
#     0xab: {0xff51: {0x11: RecordHRFrame(),  # 'recordHR'
#                     0x12: RecordSPO2Frame(),  # 'recordSPO2'
#                     0x13: RecordSTFrame(),  # 'recordST'
#                     0x14: RecordBPFrame(),  # 'recordBP'
#                     0x18: StateTagFrame(),  # 'stateTag'
#                     0x08: StateActivityFrame(),  # 'stateActivity'
#                     },
#            0xff52: RecordSleepFrame(),  # 'recordSleep'
#            0x2900: StreamPPGFrame(),  # 'streamPPG'
#            0xff31: StateHRFrame(),  # 'stateHR'
#            0xff32: StateMultiMeasureFrame(),  # 'stateMultiMeasure'
#            0xff84: StreamHRFrame(),  # 'streamHR'
#            0xff91: StatePowerFrame(),  # 'statePower'
#            0xff92: StateBandInfoFrame(),  # 'stateBandInfo'
#            # 0xff95: ControlRawEnableFrame(),  # 'raw enable'
#            # 0xff96: ControlHREnableFrame(),  # 'hr enable'
#            0xff97: StateActivationFrame(),  # 'stateActivation'
#            0xff9b: StateBandInfoExtendFrame(),  # 'stateBandInfoExtend'
#            }
# }
# =============================================================================
