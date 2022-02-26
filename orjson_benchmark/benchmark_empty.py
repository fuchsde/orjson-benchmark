# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from json import loads as json_loads
from numpy import empty

import pytest

from .json_libraries import libraries


@pytest.mark.parametrize("data", ["[]", "{}", '""'])
@pytest.mark.parametrize("library", libraries)
def test_empty(benchmark, data, library):
    dumper, loader, version = libraries[library]

    benchmark.group = f"empty deserialization"
    benchmark.name = f"{library} {version}"
    benchmark.extra_info["lib"] = library
    benchmark.extra_info["version"] = version
    benchmark.extra_info["correct"] = json_loads(dumper(loader(data))) == json_loads(data)

    benchmark(loader, data)
