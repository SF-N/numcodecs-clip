import numcodecs
import numcodecs.registry
import numpy as np
import pytest


def test_from_config():
    codec = numcodecs.registry.get_codec(dict(id="clip", minimum=0.0, maximum=1.0))
    assert codec.__class__.__name__ == "ClipCodec"
    assert codec.__class__.__module__ == "numcodecs_clip"
    assert codec.get_config() == dict(id="clip", minimum=0.0, maximum=1.0)


def test_invalid():
    with pytest.raises(ValueError):
        numcodecs.registry.get_codec(dict(id="clip", minimum=1.0, maximum=0.0))
    with pytest.raises(ValueError):
        numcodecs.registry.get_codec(dict(id="clip", minimum=np.nan))


def check_roundtrip(data: np.ndarray, minimum, maximum):
    codec = numcodecs.registry.get_codec(
        dict(id="clip", minimum=minimum, maximum=maximum)
    )

    encoded = codec.encode(data)
    np.testing.assert_array_equal(np.asarray(encoded), data)

    decoded = np.asarray(codec.decode(encoded))

    assert decoded.dtype == data.dtype
    assert decoded.shape == data.shape

    finite = np.isfinite(data)
    if minimum is not None:
        assert np.all(decoded[finite] >= minimum)
    if maximum is not None:
        assert np.all(decoded[finite] <= maximum)
    inside = finite.copy()
    if minimum is not None:
        inside &= data >= minimum
    if maximum is not None:
        inside &= data <= maximum
    np.testing.assert_array_equal(decoded[inside], data[inside])
    np.testing.assert_array_equal(np.isnan(decoded), np.isnan(data))

    out = np.empty_like(data)
    codec.decode(encoded, out=out)
    np.testing.assert_array_equal(out, decoded)


def test_roundtrip():
    data = np.linspace(-2.0, 2.0, 1001).reshape(7, 11, 13)
    check_roundtrip(data, 0.0, 1.0)
    check_roundtrip(data, None, 1.0)
    check_roundtrip(data, -1.0, None)
    check_roundtrip(data, None, None)
    check_roundtrip(np.array([np.nan, -np.inf, np.inf, 0.5]), 0.0, 1.0)
    check_roundtrip(np.arange(-10, 10, dtype=np.int32), 0, 5)
    check_roundtrip(np.zeros((0,), dtype=np.float32), 0.0, 1.0)
