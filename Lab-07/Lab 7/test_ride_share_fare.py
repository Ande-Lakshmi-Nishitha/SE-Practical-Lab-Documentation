import math
from hypothesis import given, strategies as st
from ride_share_fare import parse_trip, fare_average, payable_fare


@given(st.text() | st.none())
def test_parse_trip_no_crash(s):
    try:
        parse_trip(s)
    except Exception as e:
        assert False, f"parse_trip crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_fare_average_no_crash(s):
    try:
        fare_average(s)
    except Exception as e:
        assert False, f"fare_average crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_payable_fare_no_crash(s):
    try:
        payable_fare(s)
    except Exception as e:
        assert False, f"payable_fare crashed with: {e!r} on input {s!r}"


# ---- Extra property checks (output correctness) ----

@given(st.text() | st.none())
def test_parse_trip_output_valid(s):
    r = parse_trip(s)
    if r is not None:
        cab, km = r
        assert cab != "" and math.isfinite(km) and km >= 0


@given(st.text() | st.none())
def test_fare_average_output_valid(s):
    r = fare_average(s)
    if r is not None:
        assert isinstance(r, int) and r >= 0


@given(st.text() | st.none())
def test_payable_fare_output_valid(s):
    r = payable_fare(s)
    if r is not None:
        assert math.isfinite(r) and r >= 0


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_fare_average_valid_lists(nums):
    r = fare_average(",".join(map(str, nums)))
    assert min(nums) <= r <= max(nums)