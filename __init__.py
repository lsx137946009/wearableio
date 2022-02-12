#

__docformat__ = 'resreucturedtext'

hard_dependencies = ('numpy', 'pandas')
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from datetime import datetime

# TODO: add import
from wearableio.utils import (join_integer_decimal, 
                              join_byteblocks, 
                              join_complementary_byteblocks)
from wearableio.field import BaseField
from wearableio.frame import BaseFrame

from wearableio.sensomics.io import (read_sens_line,
                                     read_sens_stream,
                                     read_sens_text,
                                     write_json)

#
from ._version import get_versions

v = get_versions()
__version__ = v.get('closest-tag', v['version'])
__git_version__ = v.get('full-revisionid')
del get_versions, v

# TODO: add modele level doc-string
__doc__ = """
sixing liu, jianqiang gong
"""