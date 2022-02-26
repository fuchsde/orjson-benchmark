#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import json
import os
from pathlib import Path
from timeit import timeit

import orjson
import rapidjson
import simplejson
import ujson
from tabulate import tabulate

from .data import fixtures as FIXTURES
from .json_libraries import LIBRARIES, get_version
from .util import dump_string_io_to_file, read_fixture_obj

PYSORT_FILE = Path("doc/sorting/benchmark.rst")
ITERATIONS = 500


def test_sort():

    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(os.getpid(), {0, 1})

    buf = io.StringIO()
    headers = ("Library", "Version", "unsorted (ms)", "sorted (ms)", "vs. orjson")

    for fixture in sorted(FIXTURES, reverse=True):
        table = []
        buf.write(f"\n**{fixture}**\n\n")
        for lib_name in LIBRARIES:
            time_sorted, time_unsorted, compared_to_orjson = sort(f"{fixture}.xz", lib_name)

            table.append(
                (
                    lib_name,
                    get_version(lib_name),
                    f"{time_unsorted:,.2f}" if time_unsorted else "",
                    f"{time_sorted:,.2f}" if time_sorted else "",
                    f"{compared_to_orjson:,.1f}" if compared_to_orjson else "",
                )
            )

        buf.write(tabulate(table, headers, tablefmt="rst") + "\n")

    dump_string_io_to_file(PYSORT_FILE, buf)
    print(buf.getvalue())


def per_iter_latency(val):
    if val is None:
        return None
    return (val * 1000) / ITERATIONS


def sort(filename: str, lib_name: str):
    data = read_fixture_obj(filename)
    for lib_name in LIBRARIES:
        if lib_name == "json":
            time_unsorted = timeit(
                lambda: json.dumps(data).encode("utf-8"),
                number=ITERATIONS,
            )
            time_sorted = timeit(
                lambda: json.dumps(data, sort_keys=True).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "simplejson":
            time_unsorted = timeit(
                lambda: simplejson.dumps(data).encode("utf-8"),
                number=ITERATIONS,
            )
            time_sorted = timeit(
                lambda: simplejson.dumps(data, sort_keys=True).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "ujson":
            time_unsorted = timeit(
                lambda: ujson.dumps(data).encode("utf-8"),
                number=ITERATIONS,
            )
            time_sorted = timeit(
                lambda: ujson.dumps(data, sort_keys=True).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "rapidjson":
            time_unsorted = timeit(
                lambda: rapidjson.dumps(data).encode("utf-8"),
                number=ITERATIONS,
            )
            time_sorted = timeit(
                lambda: rapidjson.dumps(data, sort_keys=True).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "orjson":
            time_unsorted = timeit(lambda: orjson.dumps(data), number=ITERATIONS)
            time_sorted = timeit(
                lambda: orjson.dumps(data, None, orjson.OPT_SORT_KEYS),
                number=ITERATIONS,
            )
            orjson_time_sorted = per_iter_latency(time_sorted)
        else:
            raise NotImplementedError

        time_unsorted = per_iter_latency(time_unsorted)
        time_sorted = per_iter_latency(time_sorted)

        if lib_name == "orjson":
            compared_to_orjson = 1
        elif time_unsorted:
            compared_to_orjson = time_sorted / orjson_time_sorted
        else:
            compared_to_orjson = None
        return time_sorted, time_unsorted, compared_to_orjson
