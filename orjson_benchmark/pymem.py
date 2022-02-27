#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gc
import io
import lzma
import string
from json import loads as json_loads
from pathlib import Path

import psutil
from tabulate import tabulate

from .data import fixtures as FIXTURES
from .json_libraries import LIBRARIES, get_version
from .util import dump_string_io_to_file

BENCHMARK_MEMORY_FILE = Path("doc/memory/benchmark.rst")


def test_mem():
    buf = io.StringIO()
    headers = ("Library", "Version", "import, read() RSS (MiB)", "loads() increase in RSS (MiB)")

    for fixture in sorted(FIXTURES, reverse=True):
        table = []
        buf.write(f"\n**{fixture}**\n\n")
        for lib_name in LIBRARIES:
            file = Path(f"data/{fixture}.xz")
            output = run_memory_test(file, lib_name)
            mem_base = int(output[0]) / 1024 / 1024
            mem_diff = int(output[1]) / 1024 / 1024
            correct = bool(int(output[2]))
            if correct:
                table.append((lib_name, get_version(lib_name), f"{mem_base:,.1f}", f"{mem_diff:,.1f}"))
            else:
                table.append((lib_name, "", ""))
        buf.write(tabulate(table, headers, tablefmt="grid") + "\n")

    dump_string_io_to_file(BENCHMARK_MEMORY_FILE, buf)
    print(buf.getvalue())


def run_memory_test(filename: Path, lib_name: string):
    with lzma.open(filename, "r") as file:
        fixture = file.read()

    proc = psutil.Process()

    if lib_name == "json":
        from json import dumps, loads
    elif lib_name == "orjson":
        from orjson import dumps, loads
    elif lib_name == "rapidjson":
        from rapidjson import dumps, loads
    elif lib_name == "simplejson":
        from simplejson import dumps, loads
    elif lib_name == "ujson":
        from ujson import dumps, loads
    else:
        raise NotImplementedError

    gc.collect()
    mem_before = proc.memory_info().rss

    for _ in range(100):
        val = loads(fixture)

    mem_after = proc.memory_info().rss
    mem_diff = mem_after - mem_before

    correct = 1 if (json_loads(fixture) == json_loads(dumps(loads(fixture)))) else 0
    return mem_before, mem_diff, correct
