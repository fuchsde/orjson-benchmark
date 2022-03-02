#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

import numpy
import orjson
import pytest
import rapidjson
import simplejson

from .json_libraries import LIBRARIES, get_version


@pytest.mark.parametrize("fixture", ["int32", "float64", "bool", "int8", "uint8"])
@pytest.mark.parametrize("library", LIBRARIES)
def test_numpy(benchmark, fixture, library):

    benchmark.group = f"{fixture} dumps"
    benchmark.name = f"{library} {get_version(library)}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = get_version(library)

    if fixture == "int32":
        array = numpy.random.randint(((2**31) - 1), size=(100000, 100), dtype=numpy.int32)
    elif fixture == "float64":
        array = numpy.random.random(size=(50000, 100))
        assert array.dtype == numpy.float64
    elif fixture == "bool":
        array = numpy.random.choice((True, False), size=(100000, 200))
    elif fixture == "int8":
        array = numpy.random.randint(((2**7) - 1), size=(100000, 100), dtype=numpy.int8)
    elif fixture == "uint8":
        array = numpy.random.randint(((2**8) - 1), size=(100000, 100), dtype=numpy.uint8)
    else:
        raise NotImplementedError

    def default(__obj):
        if isinstance(__obj, numpy.ndarray):
            return __obj.tolist()

    if library == "json":
        numpy_dumps = lambda: json.dumps(array, default=default).encode("utf-8")
    elif library == "simplejson":
        numpy_dumps = lambda: simplejson.dumps(array, default=default).encode("utf-8")
    elif library == "ujson":
        numpy_dumps = None
    elif library == "rapidjson":
        numpy_dumps = lambda: rapidjson.dumps(array, default=default).encode("utf-8")
    elif library == "orjson":
        numpy_dumps = lambda: orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY)
    else:
        raise NotImplementedError

    if not json.loads(numpy_dumps()) == array.tolist():
        assert False

    benchmark(numpy_dumps)
