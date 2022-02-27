#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import io
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from tabulate import tabulate

from .json_libraries import LIBRARIES
from .util import dump_string_io_to_file


def aggregate(benchmark_src_file: Path):
    res = collections.defaultdict(dict)
    with open(benchmark_src_file, "r") as file:
        data = json.loads(file.read())

    for each in data.get("benchmarks"):
        res[each.get("group")][each.get("extra_info").get("lib")] = {
            "data": [val * 1000 for val in each.get("stats").get("data")],
            "median": each.get("stats").get("median") * 1000,
            "ops": each.get("stats").get("ops"),
            "version": each.get("extra_info").get("version"),
        }
    return res


def tab():
    benchmark_src_file = Path(sys.argv[1]) if len(sys.argv) >= 1 else Path("")

    if not benchmark_src_file.is_file():
        return

    buf = io.StringIO()
    headers = (
        "Library",
        "Version",
        "Median latency (milliseconds)",
        "Operations per second",
        "Relative (latency)",
    )
    for group, val in sorted(aggregate(benchmark_src_file).items(), reverse=True):
        buf.write(f"\n**{group}**\n\n")
        table = []
        for lib in LIBRARIES:
            table.append(
                [
                    lib,
                    val.get(lib).get("version") if val.get(lib, None) != None else None,
                    val.get(lib).get("median") if val.get(lib, None) != None else None,
                    "%.1f" % val.get(lib).get("ops") if val.get(lib, None) != None else None,
                    0,
                ]
            )
        baseline = table[0][2]
        for each in table:
            each[4] = "%.2f" % (each[2] / baseline) if isinstance(each[2], float) else None
            each[2] = "%.2f" % each[2] if isinstance(each[2], float) else None
        buf.write(tabulate(table, headers, tablefmt="rst") + "\n")

    dump_string_io_to_file(benchmark_src_file.parent / f"{benchmark_src_file.stem}.rst", buf)
    print(buf.getvalue())
