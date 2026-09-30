"""
[`ClipCodec`][numcodecs_clip.ClipCodec] for the [`numcodecs`][numcodecs] buffer compression API.
"""

__all__ = ["ClipCodec"]

import math

import numcodecs.compat
import numcodecs.registry
import numpy as np
from numcodecs.abc import Codec
from typing_extensions import Buffer  # MSPV 3.12


class ClipCodec(Codec):
    """
    Filter codec that clips the decoded values into the `[minimum, maximum]`
    range.

    Encoding passes the data through unchanged. Decoding clips every value
    below `minimum` to `minimum` and every value above `maximum` to `maximum`.
    NaN values are left untouched.

    Clipping never increases the pointwise error of a decoded value whose
    original value lies within the `[minimum, maximum]` range. This filter is
    therefore useful to restore known data limits (e.g. non-negativity or a
    `[0, 1]` range) after lossy compression, by stacking it in front of the
    lossy codec, e.g. using the
    [`numcodecs-combinators`](https://numcodecs-combinators.readthedocs.io)
    package.

    Parameters
    ----------
    minimum : None | int | float, optional
        The lower limit of the clipping range, or [`None`][None] for no lower
        limit.
    maximum : None | int | float, optional
        The upper limit of the clipping range, or [`None`][None] for no upper
        limit.
    """

    __slots__: tuple[str, ...] = ("_minimum", "_maximum")
    _minimum: None | int | float
    _maximum: None | int | float

    codec_id: str = "clip"  # type: ignore

    def __init__(
        self,
        *,
        minimum: None | int | float = None,
        maximum: None | int | float = None,
    ) -> None:
        if minimum is not None and math.isnan(minimum):
            raise ValueError("minimum must not be NaN")
        if maximum is not None and math.isnan(maximum):
            raise ValueError("maximum must not be NaN")
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum must not be greater than maximum")

        self._minimum = minimum
        self._maximum = maximum

    def encode(self, buf: Buffer) -> Buffer:
        """
        Encode the data in `buf`, which passes the data through unchanged.

        Parameters
        ----------
        buf : Buffer
            Data to be encoded. May be any object supporting the new-style
            buffer protocol.

        Returns
        -------
        enc : Buffer
            The unchanged data.
        """

        return numcodecs.compat.ensure_ndarray(buf)  # type: ignore

    def decode(self, buf: Buffer, out: None | Buffer = None) -> Buffer:
        """
        Decode the data in `buf` by clipping it into the `[minimum, maximum]`
        range.

        Parameters
        ----------
        buf : Buffer
            Data to be decoded. May be any object supporting the new-style
            buffer protocol.
        out : Buffer, optional
            Writeable buffer to store decoded data. N.B. if provided, this
            buffer must be exactly the right size to store the decoded data.

        Returns
        -------
        dec : Buffer
            Clipped data. May be any object supporting the new-style buffer
            protocol.
        """

        a = numcodecs.compat.ensure_ndarray(buf)

        if a.dtype.kind not in "iufb":
            raise TypeError(f"cannot clip data of dtype {a.dtype}")

        if self._minimum is None and self._maximum is None:
            decoded = a
        else:
            decoded = np.clip(
                a,
                a_min=None if self._minimum is None else a.dtype.type(self._minimum),
                a_max=None if self._maximum is None else a.dtype.type(self._maximum),
            )

        return numcodecs.compat.ndarray_copy(decoded, out)  # type: ignore

    def get_config(self) -> dict:
        """
        Returns the configuration of this clip codec.

        [`numcodecs.registry.get_codec(config)`][numcodecs.registry.get_codec]
        can be used to reconstruct this codec from the returned config.

        Returns
        -------
        config : dict
            Configuration of this clip codec.
        """

        return dict(
            id=type(self).codec_id,
            minimum=self._minimum,
            maximum=self._maximum,
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(minimum={self._minimum!r}, maximum={self._maximum!r})"


numcodecs.registry.register_codec(ClipCodec)
