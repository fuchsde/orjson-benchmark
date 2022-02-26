# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
from json import dumps as _json_dumps
from json import loads as json_loads

import orjson
import rapidjson
import simplejson
import ujson
from orjson import dumps as _orjson_dumps
from orjson import loads as orjson_loads
from rapidjson import dumps as _rapidjson_dumps
from rapidjson import loads as rapidjson_loads
from simplejson import dumps as _simplejson_dumps
from simplejson import loads as simplejson_loads
from ujson import dumps as _ujson_dumps
from ujson import loads as ujson_loads

LIBRARIES = ("orjson", "ujson", "rapidjson", "simplejson", "json")

# dumps wrappers that return UTF-8
def orjson_dumps(obj):
    return _orjson_dumps(obj)


def ujson_dumps(obj):
    return _ujson_dumps(obj).encode("utf-8")


def rapidjson_dumps(obj):
    return _rapidjson_dumps(obj).encode("utf-8")


def json_dumps(obj):
    return _json_dumps(obj).encode("utf-8")


def simplejson_dumps(obj):
    return _simplejson_dumps(obj).encode("utf-8")


# get version by name
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


# Add new libraries here (pair of UTF-8 dumper, loader)
libraries = {
    "orjson": (orjson_dumps, orjson_loads, get_version("orjson")),
    "ujson": (ujson_dumps, ujson_loads, get_version("ujson")),
    "json": (json_dumps, json_loads, get_version("json")),
    "rapidjson": (rapidjson_dumps, rapidjson_loads, get_version("rapidjson")),
    "simplejson": (simplejson_dumps, simplejson_loads, get_version("simplejson")),
}
