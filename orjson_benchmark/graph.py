#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import io
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
from tabulate import tabulate

from .json_libraries import LIBRARIES
from .util import dump_string_io_to_file

BENCHMARK_LATENCY_SRC_DIR = Path(".benchmarks")
BENCHMARK_LATENCY_DIR = Path("doc/performance/latency")
BENCHMARK_LATENCY_FILE = Path("benchmark.rst")


def aggregate():
    benchmarks_dir = os.path.join(BENCHMARK_LATENCY_SRC_DIR, os.listdir(BENCHMARK_LATENCY_SRC_DIR)[0])
    res = collections.defaultdict(dict)
    for filename in os.listdir(benchmarks_dir):
        with open(os.path.join(benchmarks_dir, filename), "r") as file:
            data = json.loads(file.read())

        for each in data["benchmarks"]:
            res[each["group"]][each["extra_info"]["lib"]] = {
                "data": [val * 1000 for val in each["stats"]["data"]],
                "median": each["stats"]["median"] * 1000,
                "ops": each["stats"]["ops"],
                "correct": each["extra_info"]["correct"],
                "version": each["extra_info"]["version"],
            }
    return res


def box():
    if not BENCHMARK_LATENCY_SRC_DIR.is_dir():
        return
    BENCHMARK_LATENCY_DIR.mkdir(exist_ok=True, parents=True)
    print(aggregate().items())
    for group, val in sorted(aggregate().items()):
        data, libraries_with_version = [], []
        libraries_with_version = [f"{lib}\n{val[lib]['version']}" for lib in LIBRARIES]
        for lib in LIBRARIES:
            data.append(val[lib]["data"] if val[lib]["correct"] else -1)
        fig = plt.figure(1, figsize=(9, 6))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(data, vert=False, labels=libraries_with_version)
        ax.set_xlim(left=0)
        ax.set_xlabel("milliseconds")
        plt.title(group)
        plt.savefig(BENCHMARK_LATENCY_DIR / "{}.png".format(group.replace(" ", "_").replace(".json", "")))
        plt.close()


def tab():
    if not BENCHMARK_LATENCY_SRC_DIR.is_dir():
        return
    BENCHMARK_LATENCY_DIR.mkdir(exist_ok=True, parents=True)
    buf = io.StringIO()
    headers = (
        "Library",
        "Version",
        "Median latency (milliseconds)",
        "Operations per second",
        "Relative (latency)",
    )
    for group, val in sorted(aggregate().items(), reverse=True):
        buf.write(f"\n**{group}**\n\n")
        table = []
        for lib in LIBRARIES:
            correct = val[lib]["correct"]
            version = val[lib]["version"]
            table.append(
                [
                    lib,
                    version,
                    val[lib]["median"] if correct else None,
                    "%.1f" % val[lib]["ops"] if correct else None,
                    0,
                ]
            )
        baseline = table[0][2]
        for each in table:
            each[4] = "%.2f" % (each[2] / baseline) if isinstance(each[2], float) else None
            each[2] = "%.2f" % each[2] if isinstance(each[2], float) else None
        buf.write(tabulate(table, headers, tablefmt="rst") + "\n")

    dump_string_io_to_file(BENCHMARK_LATENCY_DIR / BENCHMARK_LATENCY_FILE, buf)
    print(buf.getvalue())
