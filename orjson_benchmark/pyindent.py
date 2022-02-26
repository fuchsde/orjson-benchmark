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

PYINDENT_FILE = Path("doc/indent/benchmark.rst")


def test_indent():
    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(os.getpid(), {0, 1})

    buf = io.StringIO()
    headers = ("Library", "Version", "compact (ms)", "pretty (ms)", "vs. orjson")

    for fixture in sorted(FIXTURES, reverse=True):
        table = []
        buf.write(f"\n**{fixture}**\n\n")

        # Run once for ORJSON to get the reference
        _, time_pretty_orjson_ref, _ = indent(f"{fixture}.xz", "orjson", 1)

        for lib_name in LIBRARIES:
            time_compact, time_pretty, compared_to_orjson = indent(f"{fixture}.xz", lib_name, time_pretty_orjson_ref)

            table.append(
                (
                    lib_name,
                    get_version(lib_name),
                    f"{time_compact:,.2f}" if time_compact else "",
                    f"{time_pretty:,.2f}" if time_pretty else "",
                    f"{compared_to_orjson:,.1f}" if compared_to_orjson else "",
                )
            )

        buf.write(tabulate(table, headers, tablefmt="rst") + "\n")

    dump_string_io_to_file(PYINDENT_FILE, buf)
    print(buf.getvalue())


def indent(filename: str, lib_name: str, orjson_time_pretty_ref):
    data = read_fixture_obj(filename)
    output_in_kib_compact = len(orjson.dumps(data)) / 1024
    output_in_kib_pretty = len(orjson.dumps(data, option=orjson.OPT_INDENT_2)) / 1024

    # minimum 2s runtime for orjson compact
    ITERATIONS = int(2 / (timeit(lambda: orjson.dumps(data), number=20) / 20))

    print(f"{output_in_kib_compact:,.0f}KiB compact, {output_in_kib_pretty:,.0f}KiB pretty, {ITERATIONS} iterations")

    def per_iter_latency(val):
        if val is None:
            return None
        return (val * 1000) / ITERATIONS

    def test_correctness(serialized):
        return orjson.loads(serialized) == data

    if lib_name == "json":
        time_compact = timeit(
            lambda: json.dumps(data).encode("utf-8"),
            number=ITERATIONS,
        )
        time_pretty = timeit(
            lambda: json.dumps(data, indent=2).encode("utf-8"),
            number=ITERATIONS,
        )
        correct = test_correctness(json.dumps(data, indent=2).encode("utf-8"))
    elif lib_name == "simplejson":
        time_compact = timeit(
            lambda: simplejson.dumps(data).encode("utf-8"),
            number=ITERATIONS,
        )
        time_pretty = timeit(
            lambda: simplejson.dumps(data, indent=2).encode("utf-8"),
            number=ITERATIONS,
        )
        correct = test_correctness(simplejson.dumps(data, indent=2).encode("utf-8"))
    elif lib_name == "ujson":
        time_compact = timeit(
            lambda: ujson.dumps(data).encode("utf-8"),
            number=ITERATIONS,
        )
        time_pretty = timeit(
            lambda: ujson.dumps(data, indent=2).encode("utf-8"),
            number=ITERATIONS,
        )
        correct = test_correctness(ujson.dumps(data, indent=2).encode("utf-8"))
    elif lib_name == "rapidjson":
        time_compact = timeit(lambda: rapidjson.dumps(data), number=ITERATIONS)
        time_pretty = None
        correct = False
    elif lib_name == "orjson":
        time_compact = timeit(lambda: orjson.dumps(data), number=ITERATIONS)
        time_pretty = timeit(
            lambda: orjson.dumps(data, None, orjson.OPT_INDENT_2),
            number=ITERATIONS,
        )
        correct = test_correctness(orjson.dumps(data, None, orjson.OPT_INDENT_2))
    else:
        raise NotImplementedError

    time_compact = per_iter_latency(time_compact)
    if not correct:
        time_pretty = None
    else:
        time_pretty = per_iter_latency(time_pretty)

    if lib_name == "orjson":
        compared_to_orjson = 1
    elif time_pretty:
        compared_to_orjson = time_pretty / orjson_time_pretty_ref
    else:
        compared_to_orjson = None

    return time_compact, time_pretty, compared_to_orjson
