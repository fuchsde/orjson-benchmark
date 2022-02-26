# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from json import loads as json_loads

import pytest

from .data import fixtures
from .json_libraries import libraries
from .util import read_fixture_str


@pytest.mark.parametrize("fixture", fixtures)
@pytest.mark.parametrize("library", libraries)
def test_loads(benchmark, fixture, library):
    dumper, loader, version = libraries[library]
    
    benchmark.group = f"{fixture} deserialization"
    benchmark.name = f"{library} {version}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = version

    data = read_fixture_str(f"{fixture}.xz")
    benchmark.extra_info["correct"] = json_loads(dumper(loader(data))) == json_loads(data)

    benchmark(loader, data)
