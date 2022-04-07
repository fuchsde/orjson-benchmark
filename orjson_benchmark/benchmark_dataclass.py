#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import dataclasses
import json
from typing import List

import orjson
import pytest
import rapidjson
import simplejson
import ujson

from .json_libraries import LIBRARIES, DUMP_TO, get_version


@dataclasses.dataclass
class Member:
    id: int
    active: bool


@dataclasses.dataclass
class Object:
    id: int
    name: str
    members: List[Member]


objects_as_dataclass = [Object(i, str(i) * 3, [Member(j, True) for j in range(0, 10)]) for i in range(100000, 102000)]

objects_as_dict = [dataclasses.asdict(each) for each in objects_as_dataclass]
output_in_kib = len(orjson.dumps(objects_as_dict)) / 1024


@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_as_dict(benchmark, library, dump_to):
    benchmark.group = f"dataclass {output_in_kib:,.0f}KiB (orjson) as_dict"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    if library == "json" and dump_to == "bytes":
        as_dict = lambda: json.dumps(objects_as_dict).encode("utf-8")
    elif library == "json" and dump_to == "string":
        as_dict = lambda: json.dumps(objects_as_dict)
    elif library == "simplejson" and dump_to == "bytes":
        as_dict = lambda: simplejson.dumps(objects_as_dict).encode("utf-8")
    elif library == "simplejson" and dump_to == "string":
        as_dict = lambda: simplejson.dumps(objects_as_dict)
    elif library == "ujson" and dump_to == "bytes":
        as_dict = lambda: ujson.dumps(objects_as_dict).encode("utf-8")
    elif library == "ujson" and dump_to == "string":
        as_dict = lambda: ujson.dumps(objects_as_dict)
    elif library == "rapidjson" and dump_to == "bytes":
        as_dict = lambda: rapidjson.dumps(objects_as_dict).encode("utf-8")
    elif library == "rapidjson" and dump_to == "string":
        as_dict = lambda: rapidjson.dumps(objects_as_dict)
    elif library == "orjson" and dump_to == "bytes":
        as_dict = lambda: orjson.dumps(objects_as_dict)
    elif library == "orjson" and dump_to == "string":
        as_dict = lambda: orjson.dumps(objects_as_dict).decode("utf-8")
    else:
        raise NotImplementedError

    benchmark(as_dict)


@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_as_dataclass(benchmark, library, dump_to):
    benchmark.group = f"dataclass {output_in_kib:,.0f}KiB (orjson) as_dataclass"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    def default(__obj):
        if dataclasses.is_dataclass(__obj):
            return dataclasses.asdict(__obj)

    if library == "json" and dump_to == "bytes":
        as_dataclass = lambda: json.dumps(objects_as_dataclass, default=default).encode("utf-8")
    elif library == "json" and dump_to == "string":
        as_dataclass = lambda: json.dumps(objects_as_dataclass, default=default)
    elif library == "simplejson" and dump_to == "bytes":
        as_dataclass = lambda: simplejson.dumps(objects_as_dataclass, default=default).encode("utf-8")
    elif library == "simplejson" and dump_to == "string":
        as_dataclass = lambda: simplejson.dumps(objects_as_dataclass, default=default)
    elif library == "ujson":
        assert False
    elif library == "rapidjson" and dump_to == "bytes":
        as_dataclass = lambda: rapidjson.dumps(objects_as_dataclass, default=default).encode("utf-8")
    elif library == "rapidjson" and dump_to == "string":
        as_dataclass = lambda: rapidjson.dumps(objects_as_dataclass, default=default)
    elif library == "orjson" and dump_to == "bytes":
        as_dataclass = lambda: orjson.dumps(objects_as_dataclass, None, orjson.OPT_SERIALIZE_DATACLASS)
    elif library == "orjson" and dump_to == "string":
        as_dataclass = lambda: orjson.dumps(objects_as_dataclass, None, orjson.OPT_SERIALIZE_DATACLASS).decode("utf-8")
    else:
        raise NotImplementedError

    benchmark(as_dataclass)
