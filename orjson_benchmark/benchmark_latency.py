#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
from json import loads as json_loads

import orjson
import pytest
import rapidjson
import simplejson
import ujson

from .data import fixtures
from .json_libraries import LIBRARIES, get_version
from .util import read_fixture_str


def get_dumper_loader(library: str):
    # dumps wrappers that return UTF-8
    if library == "json":
        return lambda data: json.dumps(data).encode("utf-8"), json.loads
    elif library == "simplejson":
        return lambda data: simplejson.dumps(data).encode("utf-8"), simplejson.loads
    elif library == "ujson":
        return lambda data: ujson.dumps(data).encode("utf-8"), ujson.loads
    elif library == "rapidjson":
        return lambda data: rapidjson.dumps(data).encode("utf-8"), rapidjson.loads
    elif library == "orjson":
        return lambda data: orjson.dumps(data), orjson.loads
    else:
        raise NotImplementedError


@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("fixture", fixtures)
def test_dumps(benchmark, fixture, library):
    dumper, _ = get_dumper_loader(library)
    benchmark.group = f"{fixture} serialization"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    data = read_fixture_str(f"{fixture}.xz")
    if not json_loads(dumper(data)) == data:
        assert False

    benchmark(dumper, data)


@pytest.mark.parametrize("data", ["[]", "{}", '""'])
@pytest.mark.parametrize("library", LIBRARIES)
def test_empty(benchmark, data, library):
    dumper, loader = get_dumper_loader(library)

    benchmark.group = f"empty deserialization"
    benchmark.name = f"{library} {get_version(library)} {data}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    if not json_loads(dumper(loader(data))) == json_loads(data):
        assert False

    benchmark(loader, data)


@pytest.mark.parametrize("fixture", fixtures)
@pytest.mark.parametrize("library", LIBRARIES)
def test_loads(benchmark, fixture, library):
    dumper, loader = get_dumper_loader(library)

    benchmark.group = f"{fixture} deserialization"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    data = read_fixture_str(f"{fixture}.xz")

    if not json_loads(dumper(loader(data))) == json_loads(data):
        assert False

    benchmark(loader, data)
