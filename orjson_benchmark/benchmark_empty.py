#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from json import loads as json_loads

import pytest

from .json_libraries import libraries


@pytest.mark.parametrize("data", ["[]", "{}", '""'])
@pytest.mark.parametrize("library", libraries)
def test_empty(benchmark, data, library):
    dumper, loader, version = libraries[library]

    benchmark.group = f"empty deserialization"
    benchmark.name = f"{library} {version} {data}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = version

    if not json_loads(dumper(loader(data))) == json_loads(data):
        assert False

    benchmark(loader, data)
