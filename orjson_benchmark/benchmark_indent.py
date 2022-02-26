# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import orjson
import rapidjson
import simplejson
import ujson
import pytest

from .data import fixtures
from .json_libraries import LIBRARIES, get_version
from .util import read_fixture_obj

@pytest.mark.parametrize("fixture", fixtures)
@pytest.mark.parametrize("library", LIBRARIES)
def test_indent_compact(benchmark, fixture, library):

    benchmark.group = f"{fixture} indent compact"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(f"{fixture}.xz")

    def test_correctness(serialized):
        return json.loads(serialized) == data

    if library == "json":
        time_compact = lambda data: json.dumps(data).encode("utf-8")
        correct = test_correctness(json.dumps(data, indent=2).encode("utf-8"))
    elif library == "simplejson":
        time_compact = lambda data: simplejson.dumps(data).encode("utf-8")
        correct = test_correctness(simplejson.dumps(data, indent=2).encode("utf-8"))
    elif library == "ujson":
        time_compact = lambda data: ujson.dumps(data).encode("utf-8")
        correct = test_correctness(ujson.dumps(data, indent=2).encode("utf-8"))
    elif library == "rapidjson":
        time_compact = lambda data: rapidjson.dumps(data)
        correct = False
    elif library == "orjson":
        time_compact = lambda data: orjson.dumps(data)
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2))
    else:
        raise NotImplementedError

    benchmark.extra_info["correct"] = correct
    if correct:
        benchmark(time_compact, data)
    else:
        benchmark(None, data)

@pytest.mark.parametrize("fixture", fixtures)
@pytest.mark.parametrize("library", LIBRARIES)
def test_indent_pretty(benchmark, fixture, library):

    benchmark.group = f"{fixture} indent pretty"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(f"{fixture}.xz")

    def test_correctness(serialized):
        return json.loads(serialized) == data

    if library == "json":
        time_pretty = lambda data: json.dumps(data, indent=2).encode("utf-8")
        correct = test_correctness(json.dumps(data, indent=2).encode("utf-8"))
    elif library == "simplejson": 
        time_pretty = lambda data: simplejson.dumps(data, indent=2).encode("utf-8")
        correct = test_correctness(simplejson.dumps(data, indent=2).encode("utf-8"))
    elif library == "ujson":
        time_pretty = lambda data: ujson.dumps(data, indent=2).encode("utf-8")
        correct = test_correctness(ujson.dumps(data, indent=2).encode("utf-8"))
    elif library == "rapidjson":
        time_pretty = None
        correct = False
    elif library == "orjson":
        time_pretty = lambda data: orjson.dumps(data, None, orjson.OPT_INDENT_2)
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2))
    else:
        raise NotImplementedError

    benchmark.extra_info["correct"] = correct
    if correct:
        benchmark(time_pretty, data)
    else:
        benchmark(None, data)