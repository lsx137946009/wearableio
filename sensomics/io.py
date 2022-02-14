# -*- coding: utf-8 -*-



from collections import namedtuple
import json
import pandas as pd
from wearableio.frame import BaseFrame
from wearableio.utils import (join_integer_decimal, join_byteblocks, join_complementary_byteblocks)
# from wearableio.sensomics.settings import SENSOMICS_FRAME_TYPE
from wearableio.sensomics.frame import UnknownFrame
from wearableio.sensomics.frame import (
    StreamHRFrame, StreamPPGFrame, StreamACXFrame, StreamACYFrame, StreamACZFrame,
    RecordHRFrame, RecordSPO2Frame, RecordBPFrame, RecordSTFrame, RecordSleepFrame,
    StateTagFrame, StateHRFrame, StateActivityFrame, StateMultiMeasureFrame,
    StateActivationFrame, StatePowerFrame, StateBandInfoFrame, StateBandInfoExtendFrame)



### SENSOMICS_FRAME_TYPE
SENSOMICS_FRAME_TYPE = {
    0xa1: StreamACXFrame(),  # 'streamACX'
    0xa2: StreamACYFrame(),  # 'streamACY'
    0xa3: StreamACZFrame(),  # 'streamACZ'
    0xab: {0xff51: {0x11: RecordHRFrame(),  # 'recordHR'
                    0x12: RecordSPO2Frame(),  # 'recordSPO2'
                    0x13: RecordSTFrame(),  # 'recordST'
                    0x14: RecordBPFrame(),  # 'recordBP'
                    0x18: StateTagFrame(),  # 'stateTag'
                    0x08: StateActivityFrame(),  # 'stateActivity'
                    },
           0xff52: RecordSleepFrame(),  # 'recordSleep'
           0x2900: StreamPPGFrame(),  # 'streamPPG'
           0xff31: StateHRFrame(),  # 'stateHR'
           0xff32: StateMultiMeasureFrame(),  # 'stateMultiMeasure'
           0xff84: StreamHRFrame(),  # 'streamHR'
           0xff91: StatePowerFrame(),  # 'statePower'
           0xff92: StateBandInfoFrame(),  # 'stateBandInfo'
           # 0xff95: ControlRawEnableFrame(),  # 'raw enable'
           # 0xff96: ControlHREnableFrame(),  # 'hr enable'
           0xff97: StateActivationFrame(),  # 'stateActivation'
           0xff9b: StateBandInfoExtendFrame(),  # 'stateBandInfoExtend'
           }
}

class SensFrameParser(namedtuple('FrameParser', (('part1', 'part2', 'part3')))):

    def __new__(cls, frame, **kwags):
        # pre proces to parts
        part_slice = [slice(0, 1), slice(3, 5), slice(5, 6)]
        parts = []
        for pslice in part_slice:
            parts.append(frame[pslice])
        parts[1] = parts[1] if parts[1][0] != 0x29 else [0x29, 0x00]
        parts = list(map(lambda part: join_byteblocks(part, reverse=True), parts))
        self = super(SensFrameParser, cls).__new__(cls, *parts, **kwags)
        self.frame = frame
        return self

    def parse_type(self):
        frame_dict = SENSOMICS_FRAME_TYPE.copy()
        for key in self:
            try:
                frame_type = frame_dict[key]  # is in allowed type
            except:
                frame_obj = UnknownFrame()
                break
            if isinstance(frame_type, BaseFrame):  # is selected
                frame_obj = frame_type
                break
            elif isinstance(frame_type, dict):
                # Continue to search the next level
                frame_dict = frame_type
            else:
                frame_obj = UnknownFrame()
                break
        return frame_obj

    def parse_frame(self):
        frame = self.frame
        frame_obj = self.parse_type()
        frame_parsed = frame_obj.parse(frame, fields_out=['date', 'data'], format_out='dict')
        return frame_parsed



def read_sens_line(line):
    time, frame = line.split(';')
    # time, frame = line
    frame = json.loads(frame)  # to json list
    # parse frame and time
    frame_parsed = SensFrameParser(frame).parse_frame()
    time_parsed = {'time': int(time)}
    parsed = dict(**time_parsed, **frame_parsed)
    return parsed


def read_sens_stream(time, frame):
    # frame = json.loads(frame)  # to json list
    # parse frame and time
    frame_parsed = SensFrameParser(frame).parse_frame()
    time_parsed = {'time': int(time)}
    parsed = dict(**time_parsed, **frame_parsed)
    return parsed


def read_sens_text(filepath_or_buffer):
    fodata = open(file=filepath_or_buffer, mode='rt', encoding='utf-8')
    parsed = []
    for line in fodata:
        parsed_line = read_sens_line(line)
        parsed.append(parsed_line)
    return parsed


def write_json(filepath_or_buffer, **kwags):
    data = read_sens_text(filepath_or_buffer)
    # TODO: usd physiopandas io
    data = pd.DataFrame(data)
    data_json = data.to_json(orient='records')
    file_name = filepath_or_buffer[:-4] + '.json'
    with open(file_name, 'w') as f:
        f.write(data_json)