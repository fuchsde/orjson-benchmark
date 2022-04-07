#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
from json import loads as json_loads

import orjson
import pytest
import rapidjson
import simplejson
import ujson

from .data import FIXTURES
from .json_libraries import LIBRARIES, DUMP_TO, get_version
from .util import read_fixture_str


def get_dumper_loader(library: str, dump_to: str):
    # dumps wrappers that return UTF-8
    if library == "json" and dump_to == "bytes":
        return lambda data: json.dumps(data).encode("utf-8"), json.loads
    elif library == "json" and dump_to == "string":
        return lambda data: json.dumps(data), json.loads
    elif library == "simplejson" and dump_to == "bytes":
        return lambda data: simplejson.dumps(data).encode("utf-8"), simplejson.loads
    elif library == "simplejson" and dump_to == "string":
        return lambda data: simplejson.dumps(data), simplejson.loads
    elif library == "ujson" and dump_to == "bytes":
        return lambda data: ujson.dumps(data).encode("utf-8"), ujson.loads
    elif library == "ujson" and dump_to == "string":
        return lambda data: ujson.dumps(data), ujson.loads
    elif library == "rapidjson" and dump_to == "bytes":
        return lambda data: rapidjson.dumps(data).encode("utf-8"), rapidjson.loads
    elif library == "rapidjson" and dump_to == "string":
        return lambda data: rapidjson.dumps(data), rapidjson.loads
    elif library == "orjson" and dump_to == "bytes":
        return lambda data: orjson.dumps(data), orjson.loads
    elif library == "orjson" and dump_to == "string":
        return lambda data: orjson.dumps(data).decode("utf-8"), orjson.loads
    else:
        raise NotImplementedError


@pytest.mark.parametrize("fixture", FIXTURES)
@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_dumps(benchmark, fixture, library, dump_to):
    dumper, _ = get_dumper_loader(library, dump_to)
    benchmark.group = f"{fixture} serialization"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    data = read_fixture_str(fixture)
    if not json_loads(dumper(data)) == data:
        assert False

    benchmark(dumper, data)


@pytest.mark.parametrize("data", ["[]", "{}", '""'])
@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_empty(benchmark, data, library, dump_to):
    dumper, loader = get_dumper_loader(library, dump_to)

    benchmark.group = f"empty deserialization"
    benchmark.name = f"{library} {get_version(library)} {data} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    if not json_loads(dumper(loader(data))) == json_loads(data):
        assert False

    benchmark(loader, data)


@pytest.mark.parametrize("fixture", FIXTURES)
@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_loads(benchmark, fixture, library, dump_to):
    dumper, loader = get_dumper_loader(library, dump_to)

    benchmark.group = f"{fixture} deserialization"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    data = read_fixture_str(fixture)

    if not json_loads(dumper(loader(data))) == json_loads(data):
        assert False

    benchmark(loader, data)
