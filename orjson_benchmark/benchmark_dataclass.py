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

from .json_libraries import LIBRARIES, get_version


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
def test_as_dict(benchmark, library):
    benchmark.group = f"dataclass {output_in_kib:,.0f}KiB (orjson) as_dict"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    if library == "json":
        as_dict = lambda: json.dumps(objects_as_dict).encode("utf-8")
    elif library == "simplejson":
        as_dict = lambda: simplejson.dumps(objects_as_dict).encode("utf-8")
    elif library == "ujson":
        as_dict = lambda: ujson.dumps(objects_as_dict).encode("utf-8")
    elif library == "rapidjson":
        as_dict = lambda: rapidjson.dumps(objects_as_dict).encode("utf-8")
    elif library == "orjson":
        as_dict = lambda: orjson.dumps(objects_as_dict)
    else:
        raise NotImplementedError

    benchmark(as_dict)


@pytest.mark.parametrize("library", LIBRARIES)
def test_as_dataclass(benchmark, library):
    benchmark.group = f"dataclass {output_in_kib:,.0f}KiB (orjson) as_dataclass"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    def default(__obj):
        if dataclasses.is_dataclass(__obj):
            return dataclasses.asdict(__obj)

    if library == "json":
        as_dataclass = lambda: json.dumps(objects_as_dataclass, default=default).encode("utf-8")
    elif library == "simplejson":
        as_dataclass = lambda: simplejson.dumps(objects_as_dataclass, default=default).encode("utf-8")
    elif library == "ujson":
        assert False
    elif library == "rapidjson":
        as_dataclass = lambda: rapidjson.dumps(objects_as_dataclass, default=default).encode("utf-8")
    elif library == "orjson":
        as_dataclass = lambda: orjson.dumps(objects_as_dataclass, None, orjson.OPT_SERIALIZE_DATACLASS)
    else:
        raise NotImplementedError

    benchmark(as_dataclass)
