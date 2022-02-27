#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import lzma
import os
from configparser import ConfigParser
from functools import lru_cache
from io import StringIO
from pathlib import Path
from shutil import copyfileobj
from typing import Any

import orjson

dirname = os.path.join(os.path.dirname(__file__), "../data")


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
    config, main = ConfigParser(), "main"
    config.read("tox.ini")
    if main in config.sections():
        for key in config[main].keys():
            if "_dir" in key:
                Path(config[main][key]).mkdir(parents=True, exist_ok=True)
