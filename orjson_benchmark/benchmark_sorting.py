#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

import orjson
import pytest
import rapidjson
import simplejson
import ujson

from .data import fixtures
from .json_libraries import LIBRARIES, get_version
from .util import read_fixture_obj


@pytest.mark.parametrize("fixture", fixtures)
@pytest.mark.parametrize("library", LIBRARIES)
def test_sorted(benchmark, fixture, library):

    benchmark.group = f"{fixture} sorting sorted"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(f"{fixture}.xz")

    if library == "json":
        dumps_sorted = lambda data: json.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "simplejson":
        dumps_sorted = lambda data: simplejson.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "ujson":
        dumps_sorted = lambda data: ujson.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "rapidjson":
        dumps_sorted = lambda data: rapidjson.dumps(data, sort_keys=True).encode("utf-8")
    elif library == "orjson":
        dumps_sorted = lambda data: orjson.dumps(data, None, orjson.OPT_SORT_KEYS)
    else:
        raise NotImplementedError

    benchmark(dumps_sorted, data)


@pytest.mark.parametrize("fixture", fixtures)
@pytest.mark.parametrize("library", LIBRARIES)
def test_unsorted(benchmark, fixture, library):

    benchmark.group = f"{fixture} sorting unsorted"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)
    data = read_fixture_obj(f"{fixture}.xz")

    if library == "json":
        dumps_unsorted = lambda data: json.dumps(data).encode("utf-8")
    elif library == "simplejson":
        dumps_unsorted = lambda data: simplejson.dumps(data).encode("utf-8")
    elif library == "ujson":
        dumps_unsorted = lambda data: ujson.dumps(data).encode("utf-8")
    elif library == "rapidjson":
        dumps_unsorted = lambda data: rapidjson.dumps(data).encode("utf-8")
    elif library == "orjson":
        dumps_unsorted = lambda data: orjson.dumps(data)
    else:
        raise NotImplementedError

    benchmark(dumps_unsorted, data)
