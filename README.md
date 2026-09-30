[![image](https://img.shields.io/github/actions/workflow/status/SF-N/numcodecs-clip/ci.yml?branch=main)](https://github.com/SF-N/numcodecs-clip/actions/workflows/ci.yml?query=branch%3Amain)
[![image](https://img.shields.io/pypi/v/numcodecs-clip.svg)](https://pypi.python.org/pypi/numcodecs-clip)
[![image](https://img.shields.io/pypi/l/numcodecs-clip.svg)](https://github.com/SF-N/numcodecs-clip/blob/main/LICENSE)
[![image](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FSF-N%2Fnumcodecs-clip%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://pypi.python.org/pypi/numcodecs-clip)
[![image](https://readthedocs.org/projects/numcodecs-clip/badge/?version=latest)](https://numcodecs-clip.readthedocs.io/en/latest/?badge=latest)

# numcodecs-clip

`ClipCodec` for the [`numcodecs`] buffer compression API.

The `ClipCodec` is a filter codec: encoding passes the data through unchanged, decoding clips every value into the `[minimum, maximum]` range. Clipping never increases the error of a decoded value whose original value lies within the range, so the codec can be used to restore known data limits (e.g. non-negativity) after lossy compression:

```python
from numcodecs_clip import ClipCodec
from numcodecs_combinators import CodecStack

codec = CodecStack(
    ClipCodec(minimum=0.0, maximum=1.0),
    # ... any lossy codec ...
)
```

[`numcodecs`]: https://numcodecs.readthedocs.io/en/stable/

## License

Licensed under the Mozilla Public License, Version 2.0 ([LICENSE](LICENSE) or https://www.mozilla.org/en-US/MPL/2.0/).


## Funding

The `numcodecs-clip` package has been developed as part of [ESiWACE3](https://www.esiwace.eu), the third phase of the Centre of Excellence in Simulation of Weather and Climate in Europe.

Funded by the European Union. This work has received funding from the European High Performance Computing Joint Undertaking (JU) under grant agreement No 101093054.
