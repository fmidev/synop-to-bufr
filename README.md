# synop-to-bufr

synop2bufr.py converts given synop file to bufr file (edition 4). The resulting bufr file is based on bufr sequences 301150 and 307080.
It uses subset_arrays.py and separate_keys_and_values.py in conversion.

## Installation

Use the yum/dnf package manager to install synop-to-bufr. It can be found from fmiforge repo.

## Usage

```bash
$ python3 synop2bufr.py path/to/the/synop/file

```
