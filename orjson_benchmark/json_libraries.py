#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

import orjson
import rapidjson
import simplejson
import ujson

LIBRARIES = ("orjson", "ujson", "rapidjson", "simplejson", "json")


def get_version(library: str) -> str:
    if library == "json":
        return json.__version__
    elif library == "orjson":
        return orjson.__version__
    elif library == "rapidjson":
        return rapidjson.__version__
    elif library == "ujson":
        return ujson.__version__
    elif library == "simplejson":
        return simplejson.__version__
    else:
        return "UNKNWON"
