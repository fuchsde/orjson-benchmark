#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

import orjson
import pytest
import rapidjson
import simplejson
import ujson

from .data import FIXTURES
from .json_libraries import LIBRARIES, DUMP_TO, get_version
from .util import read_fixture_obj


@pytest.mark.parametrize("fixture", FIXTURES)
@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_sorted(benchmark, fixture, library, dump_to):

    benchmark.group = f"{fixture} sorting sorted"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(fixture)

    if library == "json" and dump_to == "bytes":
        dumps_sorted = lambda data: json.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "json" and dump_to == "string":
        dumps_sorted = lambda data: json.dumps(data, sort_keys=True)
    elif library == "simplejson" and dump_to == "bytes":
        dumps_sorted = lambda data: simplejson.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "simplejson" and dump_to == "string":
        dumps_sorted = lambda data: simplejson.dumps(data, sort_keys=True)
    elif library == "ujson" and dump_to == "bytes":
        dumps_sorted = lambda data: ujson.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "ujson" and dump_to == "string":
        dumps_sorted = lambda data: ujson.dumps(data, sort_keys=True)
    elif library == "rapidjson" and dump_to == "bytes":
        dumps_sorted = lambda data: rapidjson.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "rapidjson" and dump_to == "string":
        dumps_sorted = lambda data: rapidjson.dumps(data, sort_keys=True)
    elif library == "orjson" and dump_to == "bytes":
        dumps_sorted = lambda data: orjson.dumps(data, None, orjson.OPT_SORT_KEYS)
    elif library == "orjson" and dump_to == "string":
        dumps_sorted = lambda data: orjson.dumps(data, None, orjson.OPT_SORT_KEYS).decode("utf-8")
    else:
        raise NotImplementedError

    benchmark(dumps_sorted, data)


@pytest.mark.parametrize("fixture", FIXTURES)
@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_unsorted(benchmark, fixture, library, dump_to):

    benchmark.group = f"{fixture} sorting unsorted"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(fixture)

    if library == "json" and dump_to == "bytes":
        dumps_unsorted = lambda data: json.dumps(data).encode("utf-8")
    elif library == "json" and dump_to == "string":
        dumps_unsorted = lambda data: json.dumps(data)
    elif library == "simplejson" and dump_to == "bytes":
        dumps_unsorted = lambda data: simplejson.dumps(data).encode("utf-8")
    elif library == "simplejson" and dump_to == "string":
        dumps_unsorted = lambda data: simplejson.dumps(data)
    elif library == "ujson" and dump_to == "bytes":
        dumps_unsorted = lambda data: ujson.dumps(data).encode("utf-8")
    elif library == "ujson" and dump_to == "string":
        dumps_unsorted = lambda data: ujson.dumps(data)
    elif library == "rapidjson" and dump_to == "bytes":
        dumps_unsorted = lambda data: rapidjson.dumps(data).encode("utf-8")
    elif library == "rapidjson" and dump_to == "string":
        dumps_unsorted = lambda data: rapidjson.dumps(data)
    elif library == "orjson" and dump_to == "bytes":
        dumps_unsorted = lambda data: orjson.dumps(data)
    elif library == "orjson" and dump_to == "string":
        dumps_unsorted = lambda data: orjson.dumps(data).decode("utf-8")
    else:
        raise NotImplementedError

    benchmark(dumps_unsorted, data)
