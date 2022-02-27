#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import gc
import io
from json import loads as json_loads
from pathlib import Path

import psutil
import pytest
from tabulate import tabulate

from .data import FIXTURES
from .json_libraries import LIBRARIES, get_version
from .util import dump_string_io_to_file, read_fixture_str

BENCHMARK_MEMORY_FILE = Path("doc/memory/benchmark.rst")
HEADERS = ("Library", "Version", "import, read() RSS (MiB)", "loads() increase in RSS (MiB)")
DICT_TEST = {}


@pytest.mark.parametrize("fixture", FIXTURES)
@pytest.mark.parametrize("library", LIBRARIES)
def test_sorted(fixture, library):
    data = read_fixture_str(fixture)

    if library == "json":
        from json import dumps, loads
    elif library == "orjson":
        from orjson import dumps, loads
    elif library == "rapidjson":
        from rapidjson import dumps, loads
    elif library == "simplejson":
        from simplejson import dumps, loads
    elif library == "ujson":
        from ujson import dumps, loads
    else:
        raise NotImplementedError

    proc = psutil.Process()
    gc.collect()
    mem_before = proc.memory_info().rss
    for _ in range(100):
        val = loads(data)
    mem_after = proc.memory_info().rss
    mem_diff = mem_after - mem_before
    correct = 1 if (json_loads(data) == json_loads(dumps(loads(data)))) else 0

    mem_base = int(mem_before) / 1024 / 1024
    mem_diff = int(mem_diff) / 1024 / 1024
    correct = bool(int(correct))

    if not fixture in DICT_TEST.keys():
        DICT_TEST[fixture] = {}

    if correct:
        DICT_TEST[fixture][library] = (library, get_version(library), f"{mem_base:,.1f}", f"{mem_diff:,.1f}")
    else:
        DICT_TEST[fixture][library] = (library, get_version(library), "", "")

    if len(DICT_TEST.keys()) == len(FIXTURES):
        if all(
            [
                len(DICT_TEST[key]) == len(LIBRARIES) if type(DICT_TEST[key]) == dict else False
                for key in DICT_TEST.keys()
            ]
        ):
            buf = io.StringIO()
            for fixture in DICT_TEST.keys():
                table = []
                buf.write(f"\n**{fixture}**\n\n")
                for library in DICT_TEST[fixture]:
                    table.append(DICT_TEST[fixture][library])
                buf.write(tabulate(table, HEADERS, tablefmt="grid") + "\n")
            dump_string_io_to_file(BENCHMARK_MEMORY_FILE, buf)
            print(buf.getvalue())
