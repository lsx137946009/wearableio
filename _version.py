# -*- coding: utf-8 -*-


from warnings import catch_warnings
with catch_warnings(record=True):
    import json
import sys

version_json = '''
{
"dirty": false,
"error": null,
"full-versionid": null,
"version": "0.10.0"
}
'''

def get_versions():
    return json.loads(version_json)