Orjson-Benchmark
================
This repository is a copy of the benchmark to measure the performance and correctness of Python JSON libraries. It was copied and inspired from Orjson_.

.. _Orjson: https://github.com/ijl/orjson

The goal is, using Poetry and Tox, to simplify the execution of the test and thus enable everyone to run the benchmark quickly.

Furthermore some improvements as naming the library version used and code refactoring were added.


**Reproducing the whole benchmark:** 

.. code-block::

    poetry run tox

**Results can be found here:** 

* `Ubuntu`_
* `Windows`_
* `Macos`_

.. _Ubuntu: https://storage.googleapis.com/orjson-benchmark/doc-ubuntu-18.04.zip 
.. _Windows: https://storage.googleapis.com/orjson-benchmark/doc-windows-latest.zip
.. _Macos: https://storage.googleapis.com/orjson-benchmark/doc-macos-latest.zip

Types
================
dataclass
~~~~~~~~~~~
**Reproducing:** 

.. code-block::

    poetry run tox -e setup,update,dataclass

datetime
~~~~~~~~~~~
No benchmark available.

enum
~~~~~~~~~~~
No benchmark available.

float
~~~~~~~~~~~
No benchmark available.

int
~~~~~~~~~~~
No benchmark available.

numpy
~~~~~~~~~~~
**Reproducing:** 

.. code-block::

    poetry run tox -e setup,update,numpy

str
~~~~~~~~~
No benchmark available.

nonstr
~~~~~~~~~
No benchmark available.

uuid
~~~~~~~~~
No benchmark available.

Correctness
================
No benchmark available.

Performance
================
Serialization and deserialization performance of orjson is better than ultrajson, rapidjson, simplejson, or json. The benchmarks are done on fixtures of real data:

* twitter.json, 631.5KiB, results of a search on Twitter for "一", containing CJK strings, dictionaries of strings and arrays of dictionaries, indented.

* github.json, 55.8KiB, a GitHub activity feed, containing dictionaries of strings and arrays of dictionaries, not indented.

* citm_catalog.json, 1.7MiB, concert data, containing nested dictionaries of strings and arrays of integers, indented.

* canada.json, 2.2MiB, coordinates of the Canadian border in GeoJSON format, containing floats and arrays, indented.

Latency
~~~~~~~~~~~
**Reproducing:** 

.. code-block::

    poetry run tox -e setup,update,latency-dumps,latency-empty,latency-loads

Memory
~~~~~~~~~~~
**Reproducing:** 

.. code-block::

    poetry run tox -e setup,update,memory

Other
================
Sorting
~~~~~~~~~~~
**Reproducing:** 

.. code-block::

    poetry run tox -e setup,update,sort


Indent
~~~~~~~~~~~
**Reproducing:** 

.. code-block::

    poetry run tox -e setup,update,indent
