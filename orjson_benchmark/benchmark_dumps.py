#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from json import loads as json_loads

import pytest

from .data import fixtures
from .json_libraries import libraries
from .util import read_fixture_str


@pytest.mark.parametrize("library", libraries)
@pytest.mark.parametrize("fixture", fixtures)
def test_dumps(benchmark, fixture, library):
    dumper, _, version = libraries[library]

    benchmark.group = f"{fixture} serialization"
    benchmark.name = f"{library} {version}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = version

    data = read_fixture_str(f"{fixture}.xz")
    if not json_loads(dumper(data)) == data:
        assert False

    benchmark(dumper, data)
