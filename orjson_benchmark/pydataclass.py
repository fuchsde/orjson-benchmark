#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import dataclasses
import io
import json
import os
from pathlib import Path
from timeit import timeit
from typing import List

import orjson
import rapidjson
import simplejson
import ujson
from tabulate import tabulate

from .json_libraries import LIBRARIES, get_version
from .util import dump_string_io_to_file

PYDATACLASS_FILE = Path("doc/types/dataclass/benchmark.rst")
ITERATIONS = 100


def test_dataclass():

    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(os.getpid(), {0, 1})

    @dataclasses.dataclass
    class Member:
        id: int
        active: bool

    @dataclasses.dataclass
    class Object:
        id: int
        name: str
        members: List[Member]

    objects_as_dataclass = [
        Object(i, str(i) * 3, [Member(j, True) for j in range(0, 10)]) for i in range(100000, 102000)
    ]

    objects_as_dict = [dataclasses.asdict(each) for each in objects_as_dataclass]

    output_in_kib = len(orjson.dumps(objects_as_dict)) / 1024

    print(f"{output_in_kib:,.0f}KiB output (orjson)")

    def default(__obj):
        if dataclasses.is_dataclass(__obj):
            return dataclasses.asdict(__obj)

    headers = ("Library", "Version", "dict (ms)", "dataclass (ms)", "vs. orjson")

    def per_iter_latency(val):
        if val is None:
            return None
        return (val * 1000) / ITERATIONS

    table = []
    for lib_name in LIBRARIES:
        if lib_name == "json":
            as_dict = timeit(
                lambda: json.dumps(objects_as_dict).encode("utf-8"),
                number=ITERATIONS,
            )
            as_dataclass = timeit(
                lambda: json.dumps(objects_as_dataclass, default=default).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "simplejson":
            as_dict = timeit(
                lambda: simplejson.dumps(objects_as_dict).encode("utf-8"),
                number=ITERATIONS,
            )
            as_dataclass = timeit(
                lambda: simplejson.dumps(objects_as_dataclass, default=default).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "ujson":
            as_dict = timeit(
                lambda: ujson.dumps(objects_as_dict).encode("utf-8"),
                number=ITERATIONS,
            )
            as_dataclass = None
        elif lib_name == "rapidjson":
            as_dict = timeit(
                lambda: rapidjson.dumps(objects_as_dict).encode("utf-8"),
                number=ITERATIONS,
            )
            as_dataclass = timeit(
                lambda: rapidjson.dumps(objects_as_dataclass, default=default).encode("utf-8"),
                number=ITERATIONS,
            )
        elif lib_name == "orjson":
            as_dict = timeit(lambda: orjson.dumps(objects_as_dict), number=ITERATIONS)
            as_dataclass = timeit(
                lambda: orjson.dumps(objects_as_dataclass, None, orjson.OPT_SERIALIZE_DATACLASS),
                number=ITERATIONS,
            )
            orjson_as_dataclass = per_iter_latency(as_dataclass)
        else:
            raise NotImplementedError

        as_dict = per_iter_latency(as_dict)
        as_dataclass = per_iter_latency(as_dataclass)

        if lib_name == "orjson":
            compared_to_orjson = 1
        elif as_dataclass:
            compared_to_orjson = int(as_dataclass / orjson_as_dataclass)
        else:
            compared_to_orjson = None

        table.append(
            (
                lib_name,
                get_version(lib_name),
                f"{as_dict:,.2f}" if as_dict else "",
                f"{as_dataclass:,.2f}" if as_dataclass else "",
                f"{compared_to_orjson:d}" if compared_to_orjson else "",
            )
        )

    buf = io.StringIO()
    buf.write(f"**dataclass** - {output_in_kib:,.0f}KiB output (orjson)\n\n")
    buf.write(tabulate(table, headers, tablefmt="rst") + "\n")

    dump_string_io_to_file(PYDATACLASS_FILE, buf)
    print(buf.getvalue())
