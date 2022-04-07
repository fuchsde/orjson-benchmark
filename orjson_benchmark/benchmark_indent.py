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
def test_compact(benchmark, fixture, library, dump_to):

    benchmark.group = f"{fixture} indent compact"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(fixture)

    def test_correctness(serialized):
        return json.loads(serialized) == data

    if library == "json" and dump_to == "bytes":
        time_compact = lambda data: json.dumps(data).encode("utf-8")
        correct = test_correctness(json.dumps(data, indent=2).encode("utf-8"))
    elif library == "json" and dump_to == "string":
        time_compact = lambda data: json.dumps(data)
        correct = test_correctness(json.dumps(data, indent=2))
    elif library == "simplejson" and dump_to == "bytes":
        time_compact = lambda data: simplejson.dumps(data).encode("utf-8")
        correct = test_correctness(simplejson.dumps(data, indent=2).encode("utf-8"))
    elif library == "simplejson" and dump_to == "string":
        time_compact = lambda data: simplejson.dumps(data)
        correct = test_correctness(simplejson.dumps(data, indent=2))
    elif library == "ujson" and dump_to == "bytes":
        time_compact = lambda data: ujson.dumps(data).encode("utf-8")
        correct = test_correctness(ujson.dumps(data, indent=2).encode("utf-8"))
    elif library == "ujson" and dump_to == "string":
        time_compact = lambda data: ujson.dumps(data)
        correct = test_correctness(ujson.dumps(data, indent=2))
    elif library == "rapidjson":
        time_compact = lambda data: rapidjson.dumps(data)
        correct = False
    elif library == "orjson" and dump_to == "bytes":
        time_compact = lambda data: orjson.dumps(data)
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2))
    elif library == "orjson" and dump_to == "string":
        time_compact = lambda data: orjson.dumps(data).decode("utf-8")
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2).decode("utf-8"))
    else:
        raise NotImplementedError

    if not correct:
        assert False

    benchmark(time_compact, data)


@pytest.mark.parametrize("fixture", FIXTURES)
@pytest.mark.parametrize("library", LIBRARIES)
@pytest.mark.parametrize("dump_to", DUMP_TO)
def test_pretty(benchmark, fixture, library, dump_to):

    benchmark.group = f"{fixture} indent pretty"
    benchmark.name = f"{library} {get_version(library)} to {dump_to}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(fixture)

    def test_correctness(serialized):
        return json.loads(serialized) == data

    if library == "json" and dump_to == "bytes":
        time_pretty = lambda data: json.dumps(data, indent=2).encode("utf-8")
        correct = test_correctness(json.dumps(data, indent=2).encode("utf-8"))
    elif library == "json" and dump_to == "string":
        time_pretty = lambda data: json.dumps(data, indent=2)
        correct = test_correctness(json.dumps(data, indent=2))
    elif library == "simplejson" and dump_to == "bytes":
        time_pretty = lambda data: simplejson.dumps(data, indent=2).encode("utf-8")
        correct = test_correctness(simplejson.dumps(data, indent=2).encode("utf-8"))
    elif library == "simplejson" and dump_to == "string":
        time_pretty = lambda data: simplejson.dumps(data, indent=2)
        correct = test_correctness(simplejson.dumps(data, indent=2))
    elif library == "ujson" and dump_to == "bytes":
        time_pretty = lambda data: ujson.dumps(data, indent=2).encode("utf-8")
        correct = test_correctness(ujson.dumps(data, indent=2).encode("utf-8"))
    elif library == "ujson" and dump_to == "string":
        time_pretty = lambda data: ujson.dumps(data, indent=2)
        correct = test_correctness(ujson.dumps(data, indent=2))
    elif library == "rapidjson":
        time_pretty = None
        correct = False
    elif library == "orjson" and dump_to == "bytes":
        time_pretty = lambda data: orjson.dumps(data, None, orjson.OPT_INDENT_2)
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2))
    elif library == "orjson" and dump_to == "string":
        time_pretty = lambda data: orjson.dumps(data, None, orjson.OPT_INDENT_2).decode("utf-8")
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2).decode("utf-8"))
    else:
        raise NotImplementedError

    if not correct:
        assert False

    benchmark(time_pretty, data)
