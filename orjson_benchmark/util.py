# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import lzma
import os
from functools import lru_cache
from io import StringIO
from pathlib import Path
from shutil import copyfileobj
from typing import Any

import orjson

dirname = os.path.join(os.path.dirname(__file__), "../data")

if hasattr(os, "sched_setaffinity"):
    os.sched_setaffinity(os.getpid(), {0, 1})


@lru_cache(maxsize=None)
def read_fixture_str(filename: str) -> str:
    path = Path(dirname, filename)
    if path.suffix == ".xz":
        contents = lzma.decompress(path.read_bytes())
    else:
        contents = path.read_bytes()
    return contents.decode("utf-8")


@lru_cache(maxsize=None)
def read_fixture_obj(filename: str) -> Any:
    return orjson.loads(read_fixture_str(filename))


def dump_string_io_to_file(filename: Path, buf: StringIO):
    filename.parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w") as file:
        buf.seek(0)
        copyfileobj(buf, file)


def create_doc_folders():
    print("FIXUTRE!")
    Path("doc/indent").mkdir(parents=True, exist_ok=True)
    Path("doc/latency/dumps").mkdir(parents=True, exist_ok=True)
    Path("doc/latency/empty").mkdir(parents=True, exist_ok=True)
    Path("doc/latency/loads").mkdir(parents=True, exist_ok=True)
    Path("doc/memory").mkdir(parents=True, exist_ok=True)
    Path("doc/sorting").mkdir(parents=True, exist_ok=True)
    Path("doc/types/dataclass").mkdir(parents=True, exist_ok=True)
    Path("doc/types/numpy").mkdir(parents=True, exist_ok=True)
